import dash
import dash_core_components as dcc
import dash_html_components as html


title = html.Div([
    html.Div(
        [html.H1("Twitch Stream Live Analytics", id = "app_name")],
        className = "d-flex justify-content-center"
    )],
    className = "row"
)

wordcloud_component = html.Div(
    [
        html.H2("Wordcloud"),
        html.Img(id = "wordcloud", className = "flex rounded")
    ],
    className = "col-6"
)

feed_component = html.Div(
    [
        html.H2("Chat", style = {"text-decoration": "underline"}),
        html.Div(id = "message_stream", className = "container min-width-460-md")
    ],
    className = "col-6 rounded",
    style = {"border" : "solid"}
)


intervals_components = [
    dcc.Interval(
            id = "feed-interval-component", 
            interval = 1000 * 0.5, 
            n_intervals = 0
        ),
    dcc.Interval(
            id = "wordcloud-interval-component", 
            interval = 1000 * 5, 
            n_intervals = 0
        )
]

body = html.Div([
    html.Div([
        wordcloud_component,
        feed_component,
        ],
        className = "row"
    ),
    *intervals_components],
    className = "container"
)

footer = html.Footer("")

layout = html.Div([title, body, footer], className = "container")
