import dash
from dash import html
from dash    import dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
from graph import graph

app = dash.Dash(__name__)
functions = ["Add node", "Delete node", "Add edge","Delete edge","Path", "Suggestions", "Check node", "Check edge"]
GraphObj = graph()
def refreshElements():   
    nodes = [
        {
            'data': {'id': str(key[0]), 'label': key[1]},
            'classes': ''
        }

        for key in GraphObj.graph
        
    ]

    edges = [
        {
            'data': {'source': str(source[0]), 'target': str(target)},
            'classes':''
        }
        
        for source, value in GraphObj.graph.items()
        for target in value
    ]
    return nodes + edges


cyto.load_extra_layouts()

app.layout = html.Div([
    html.H1("Grafo - Proyecto Final"),
    html.Div([
        dcc.Dropdown(
            id='options',
            options=[
                {'label': option, 'value': option} for option in functions
            ],
            value='add node'
        )], style={'width':'15%', 'display': 'inline-block', 'marginRight':'5%', 'marginLeft':'1%'}
    ),
    html.Div(
        [
        html.P(children=[], id='TitleInput1', style={'fontSize':'17px'}),
        dcc.Input(id='valor-1', value='', type='text')
    ], style={'display':'inline-block'}),
    html.Div(
        [
        html.P(children=[], id='TitleInput2', style={'fontSize':'17px'}),
        dcc.Input(id='valor-2', value='', type='text')
    ],id= 'Input2', style={'display':'inline-block', 'margin':'1%'}),
    html.Div([
        html.Button(id='submit', children='submit', n_clicks=0)
    ], style={'display':'inline-block'}),
    html.Div(id='textOutput', style={'display':'inline-block', 'marginLeft': '10%'}),
    cyto.Cytoscape(
        id='cytoscape',
        elements= refreshElements(),
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '800px'},
        stylesheet=[
            {
                'selector' : '.red',
                'style':{
                    'background-color':'red',
                    'line-color':'red'
                }
            },
            {
                'selector': '.blue',
                'style':{
                    'background-color':'blue'
                }
            },
            {
                'selector': 'node',
                'style':{
                    'content': 'data(label)'
                }
            }
        ]
    )
])


@app.callback(
    Output('cytoscape', 'elements'),
    Output('textOutput', 'children'),
    State('options', 'value'),
    State('valor-1', 'value'),
    State('valor-2', 'value'),
    State('cytoscape', 'elements'),
    Input('submit', 'n_clicks')
)
def graphOptions(option, valor1, valor2, elements, btn):
    text = ""
    if valor1:
        if option == functions[0] and valor2:
            if GraphObj.addNodeManual(int(valor1), valor2):
                text = "El nodo ha sido agregado"
            else:
                text = "El nodo ya existe"
        elif option == functions[1]:
            if GraphObj.deleteNode(int(valor1)):
                text = "El nodo ha sido eliminado"
            else:
                text = "El nodo no existe"
        elif option == functions[2] and valor2:
            if GraphObj.addEdgeManual(int(valor1), int(valor2)):
                text = "La relación entre los nodos " + valor1 + " y " + valor2 + " ha sido agregada"
            else:
                text = "La relación entre los nodos no pudo ser realizada"
        elif option == functions[3] and valor2:
            if GraphObj.deleteEdge(int(valor1), int(valor2)):
                text = "La relación ha sido eliminada"
            else:
                text = "No se ha podido realizar la eliminación de relación"
        elif option == functions[4] and valor2:
            text = str(GraphObj.shortestPath(int(valor1), int(valor2)))
        elif option == functions[5]:
            text = str(GraphObj.suggestedRelations(int(valor1)))
        elif option == functions[6]:
            if GraphObj.checkNode(int(valor1)):
                text = "El nodo existe en el grafo"
            else:
                text = "El nodo no existe en el grafo"
        elif option == functions[7]:
            if GraphObj.checkEdge(int(valor1), int(valor2)):
                text = "La relación existe"
            else:
                text = "Relación no encontrada"
    elements = refreshElements()
    return elements, text
    
@app.callback(
    Output('TitleInput1', 'children'),
    Output('TitleInput2', 'children'),
    Output('Input2', 'style'),
    Input('options', 'value'),
    Input('Input2', 'style')
)
def titleInputs(currentOption, secondInputStyle):
    titleInput1 = ""
    titleInput2 = ""
    if currentOption == functions[0]:
        secondInputStyle["display"] = secondInputStyle["display"].replace("none", "inline-block ")
        titleInput1 = "ID"
        titleInput2 = "Usuario"
    elif currentOption == functions[2] or currentOption == functions[3] or currentOption == functions[4] or currentOption == functions[7]:
        secondInputStyle["display"] = secondInputStyle["display"].replace("none", "inline-block ")
        titleInput1 = "ID nodo 1"
        titleInput2 = "ID nodo 2"
    elif currentOption == functions[6] or currentOption == functions[1] or currentOption == functions[5]:
        secondInputStyle["display"] = secondInputStyle["display"].replace("inline-block", "none")
        titleInput1 = "ID nodo"
    return titleInput1, titleInput2, secondInputStyle

app.run_server(debug=True)