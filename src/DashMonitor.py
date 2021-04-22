import argparse

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


from io import BytesIO
import base64
from wordcloud import WordCloud

import preprocessing
# Import layout
from layout import layout

# DEV
import numpy as np

# Notes :

# - Interval does NOT preserve message order when displaying div's !
#   - OK for WordCount / WordCloud
#   - KO for Chat follow


parser = argparse.ArgumentParser()
parser.add_argument("--channel")
parser.add_argument("--redis_host")
args = parser.parse_args()

app = dash.Dash(
    "TwitchStream :" + args.channel, 
    external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"]
)


@app.callback(Output('message_stream', "children"),
    [Input('feed-interval-component', "n_intervals")],
    [State('message_stream', 'children')]
)
def update_feed(n, msg_stream_state):
    
    # Broken : removed by sink
    if not msg_stream_state:
        print("Test 1")
        return html.Div("No new message in stream !", id = "no_new_message")

    elif msg_stream_state['props']['id'] != "no_new_message":

        feed_client.run()
        data = feed_client.data
        print("FEED :")
        print(data)
        data = sorted(data, key = lambda x: x['timestamp'], reverse = True)

        max_msg = 15
        if len(data) >= max_msg:
            data = data[-max_msg:]

        if len(data) > 0:
            if msg_stream_state['props']['id'] != "no_new_message":
                data.pop(0) # for sink

        new_msg_stream = format_stream_data(data)
        return html.Div(new_msg_stream, id = "new_message_stream")
    else:
        print("Test 2")
        return html.Div("No new message in stream !", id = "no_new_message")

@app.callback(Output('wordcloud', 'src'),
    [Input('wordcloud-interval-component', "n_intervals")])
def update_wordcloud(n):

    client.run()
    data = client.wordcount
    wordcloud = format_wordcount(data)
    img = BytesIO()
    wordcloud.save(img, format = "PNG")
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

def format_wordcount(data):

    """
    Format wordcount from Redis to Wordcloud image
    """

    size = 500

    x, y = np.ogrid[:size, :size]
    mask = (x - (size / 2)) ** 2 + (y - (size / 2)) ** 2 > 250 ** 2
    mask = 255 * mask.astype(int)

    wc = WordCloud(
        background_color='black', 
        width=500, 
        height=500,
        mask = mask
    )
    wc.generate_from_frequencies(data)
    return wc.to_image()


def format_stream_data(data):
    comps = [html.Div(row['user'] + " : " + row['text']) for row in reversed(data)]
    container = html.Div(comps)
    return container


if __name__ == "__main__":

    client = preprocessing.Processor(
        args.channel, 
        args.redis_host, 
        redis_tables = ["categoryCount", "wordcount", "sentiment_counts"]
        )
    client.run()

    feed_client = preprocessing.Processor(
        args.channel, 
        args.redis_host, redis_tables = ["raw"]
        )
    feed_client.run()

    app.layout = layout
    app.run_server("0.0.0.0", debug = True)
