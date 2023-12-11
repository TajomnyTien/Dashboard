import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default = "notebook"
import folium
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import random 
import re



#data / nahraj cestu
data_VI = pd.read_excel("C:/Users/vladimir.tesar/Desktop/Interactive_Dashboard/0818_DALV_2023_final_opravene.xlsx", sheet_name = "DALV - VI")
data_VA = pd.read_excel("C:/Users/vladimir.tesar/Desktop/Interactive_Dashboard/0818_DALV_2023_final_opravene.xlsx", sheet_name = "DALV - VA")

###data pre ciselne kody
rezort = {
    'Číselný kód': [
        '03', '10', '11', '12', '13', '15', '18', '20', '21', '22', '24', '26', '99'],
    'Názov': [
        'Úrad vlády SR - Min. pôdohospodárstva a rozvoja vidieka SR',
        'Ministerstvo zahraničných vecí SR - Min. dopravy, výstavby a reg. rozvoja SR',
        'Ministerstvo obrany SR - Úrad geodézie, kartografie a katastra SR',
        'Ministerstvo vnútra SR - Štatistický úrad SR',
        'Ministerstvo spravodlivosti SR - Úrad pre verejné obstarávanie',
        'Ministerstvo financií SR - Úrad jadrového dozoru SR',
        'Ministerstvo životného prostredia SR - Úrad priemyselného vlastníctva SR',
        'Min. školstva, vedy, výskumu a športu SR - Úrad pre normal., metrológiu a skúšobníctvo SR',
        'Ministerstvo zdravotníctva SR - Protimonopolný úrad SR',
        'Min. práce, sociálnych vecí a rodiny SR - Národný bezpečnostný úrad',
        'Ministerstvo kultúry SR - Správa štátnych hmotných rezerv SR',
        'Ministerstvo hospodárstva SR - Národný inšpektorát práce',
        'bez príslušnosti k orgánu štátnej správy']
}

pravna_forma = {
    'Číselný kód': [
        '110', '111', '112', '113', '117', '118', '119', '121', '205', '301',
        '311', '312', '321', '331', '381', '382', '421', '422', '999'],
    'Názov': [
        'podnikateľ - fyzická osoba', 'verejná obchodná spoločnosť', 'spoločnosť s ručením obmedzeným', 'združenie (zväz, spolok, spoločnosť, klub)', 'nadácia',
        'neinvestičný fond', 'nezisková organizácia', 'akciová spoločnosť', 'družstvo', 'štátny podnik',
        'Národná banka Slovenska', 'banka - štátny peňažný ústav', 'rozpočtová organizácia', 'príspevková organizácia', 'fond rozhlasová, tlačová a televízna agentúra',
        'verejnoprávna inštitúcia', 'zahranič.osoba (práv.os. so sídl. mimo SR)', 'zahranič.osoba (fyz.os. s bydl. mimo SR)', 'iná právna forma']
}

VI = {
    'Číselný kód': [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 99],
    'Názov': [
        'stredná škola', 'vysoká škola', 'VI orgánov štátnej správy', 'VI obcí a miest',
        'VI stavovských organizácií a profesijných zväzov', 'VI družstiev', 'VI občianskych a záujmových združení',
        'VI odborových organizácií', 'VI cirkví a náboženských spoločností', 'VI kultúrnych ustanovizní',
        'VI zamestnávateľov', 'VI iná']
}

# vsetky cisla okresov
data_okresy = {
    "Číselný kód": [101, 102, 103, 104, 105, 106, 107, 108, 201, 202, 203, 204, 205, 206, 207, 301, 302, 303, 304, 305, 306, 307, 308, 309, 401, 402, 403, 404, 405, 406, 407, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811],
    "Úplný názov": ["Okres Bratislava I", "Okres Bratislava II", "Okres Bratislava III", "Okres Bratislava IV", "Okres Bratislava V", "Okres Malacky", "Okres Pezinok", "Okres Senec", "Okres Dunajská Streda", "Okres Galanta", "Okres Hlohovec", "Okres Piešťany", "Okres Senica", "Okres Skalica", "Okres Trnava", "Okres Bánovce nad Bebravou", "Okres Iľava", "Okres Myjava", "Okres Nové Mesto nad Váhom", "Okres Partizánske", "Okres Považská Bystrica", "Okres Prievidza", "Okres Púchov", "Okres Trenčín", "Okres Komárno", "Okres Levice", "Okres Nitra", "Okres Nové Zámky", "Okres Šaľa", "Okres Topoľčany", "Okres Zlaté Moravce", "Okres Bytča", "Okres Čadca", "Okres Dolný Kubín", "Okres Kysucké Nové Mesto", "Okres Liptovský Mikuláš", "Okres Martin", "Okres Námestovo", "Okres Ružomberok", "Okres Turčianske Teplice", "Okres Tvrdošín", "Okres Žilina", "Okres Banská Bystrica", "Okres Banská Štiavnica", "Okres Brezno", "Okres Detva", "Okres Krupina", "Okres Lučenec", "Okres Poltár", "Okres Revúca", "Okres Rimavská Sobota", "Okres Veľký Krtíš", "Okres Zvolen", "Okres Žarnovica", "Okres Žiar nad Hronom", "Okres Bardejov", "Okres Humenné", "Okres Kežmarok", "Okres Levoča", "Okres Medzilaborce", "Okres Poprad", "Okres Prešov", "Okres Sabinov", "Okres Snina", "Okres Stará Ľubovňa", "Okres Stropkov", "Okres Svidník", "Okres Vranov nad Topľou", "Okres Gelnica", "Okres Košice I", "Okres Košice II", "Okres Košice III", "Okres Košice IV", "Okres Košice-okolie", "Okres Michalovce", "Okres Rožňava", "Okres Sobrance", "Okres Spišská Nová Ves", "Okres Trebišov"],
    "Skrátený názov": ["Bratislava I", "Bratislava II", "Bratislava III", "Bratislava IV", "Bratislava V", "Malacky", "Pezinok", "Senec", "Dunajská Streda", "Galanta", "Hlohovec", "Piešťany", "Senica", "Skalica", "Trnava", "Bánovce nad Bebravou", "Iľava", "Myjava", "Nové Mesto nad Váhom", "Partizánske", "Považská Bystrica", "Prievidza", "Púchov", "Trenčín", "Komárno", "Levice", "Nitra", "Nové Zámky", "Šaľa", "Topoľčany", "Zlaté Moravce", "Bytča", "Čadca", "Dolný Kubín", "Kysucké Nové Mesto", "Liptovský Mikuláš", "Martin", "Námestovo", "Ružomberok", "Turčianske Teplice", "Tvrdošín", "Žilina", "Banská Bystrica", "Banská Štiavnica", "Brezno", "Detva", "Krupina", "Lučenec", "Poltár", "Revúca", "Rimavská Sobota", "Veľký Krtíš", "Zvolen", "Žarnovica", "Žiar nad Hronom", "Bardejov", "Humenné", "Kežmarok", "Levoča", "Medzilaborce", "Poprad", "Prešov", "Sabinov", "Snina", "Stará Ľubovňa", "Stropkov", "Svidník", "Vranov nad Topľou", "Gelnica", "Košice I", "Košice II", "Košice III", "Košice IV", "Košice-okolie", "Michalovce", "Rožňava", "Sobrance", "Spišská Nová Ves", "Trebišov"]
}

# vsetky cisla krajov
data_kraje = {
    "Číselný kód": [100, 200, 300, 400, 500, 600, 700, 800],
    "Úplný názov": ["Bratislavský kraj", "Trnavský kraj", "Trenčiansky kraj", "Nitriansky kraj", 
                    "Žilinský kraj", "Banskobystrický kraj", "Prešovský kraj", "Košický kraj"],
    "Skrátený názov": ["Bratislavský", "Trnavský", "Trenčiansky", "Nitriansky", "Žilinský", "Banskobystrický", "Prešovský", "Košický"]
}

vlastnictvo = {
    'Číselný kód': [1, 2, 3, 4, 5, 6, 7, 8],
    'Názov': [
        'medzinárodné s prevažujúcim verejným sektorom',
        'súkromné tuzemské',
        'družstevné',
        'štátne',
        'vlastníctvo územnej samosprávy',
        'vlastníctvo združení, politických strán a cirkví',
        'zahraničné',
        'medzinárodné s prevažne súkromným sektorom']
}

obsah_vzdelávania = """Široko vymedzené
odbory
vzdelávania
Úzko vymedzené odbory vzdelávania Podrobne vymedzené odbory vzdelávania
0 Všeobecné
vzdelávanie
01 Všeobecno-vzdelávacie programy 0100 Všeobecno-vzdelávacie programy
08 Čítanie, písanie a počítanie 0800 Čítanie, písanie a počítanie
09 Osobné zručnosti 0900 Osobné zručnosti
1 Výchova a
vzdelávanie
14 Príprava učiteľov a pedagogika 1400 Príprava učiteľov a pedagogika – širšie
programy
1420 Pedagogika
1430 Príprava učiteľov pre materské školy
1440 Príprava učiteľov pre zákl. vzdelávanie
1450 Príprava učiteľov všeobecno-
vzdelávacích predmetov
1460 Príprava učiteľov odborných predmetov
2 Humanitné
vedy a umenie
21 Umenie 2100 Umenie – širšie programy
2110 Výtvarné umenie
2120 Hudba a divadelné (interpretač.) umenie
2130 Audiovizuálna technika a mediálna
výroba a produkcia
2140 Dizajn
2150 Umelecko-remeselné zručnosti
22 Humanitné vedy 2200 Humanitné vedy – širšie programy
2210 Náboženstvo
2221 Cudzie jazyky - anglický
2222 Cudzie jazyky - nemecký
2223 Cudzie jazyky - francúzsky
2224 Cudzie jazyky - španielsky
2225 Cudzie jazyky - iný
2230 Materinský jazyk
2250 História a archeológia
2260 Filozofia a etika
3 Spoločenské
vedy,
31 Spoločenské vedy a vedy
o človeku a jeho konaní
3100 Spoločenské vedy a vedy o človeku
a jeho konaní – širšie programy
ekonómia 3110 Psychológia
a právo 3120 Sociológia a kulturológia
3130 Politické vedy a občianska náuka
3140 Ekonómia
32 Žurnalistika a informácie 3210 Žurnalistika a spravodajstvo
3220 Knihovníctvo, informácií a archívnictvo
34 Ekonomika, riadenie a správa 3400 Ekonomika, riadenie a správa – širšie
programy
3410 Veľkoobchod a maloobchod
3420 Marketing a propagácia
3430 Finančníctvo, bankovníctvo a poisťovn.
3440 Účtovníctvo a dane
3450 Manažment a správa
3460 Sekretárske a kancelárske práce
3470 Pracovné prostredie
38 Právo 3800 Právo
4 Prírodné vedy, 42 Vedy o živej prírode 4210 Biológia a biochémia
matematika a 4220 Veda o životnom prostredí
informatika 44 Vedy o neživej prírode 4400 Vedy o neživej prírode – širšie programy
4410 Fyzika
4420 Chémia
4430 Vedy o Zemi
2
Široko vymedzené
odbory
vzdelávania
Úzko vymedzené
odbory vzdelávania
Podrobne vymedzené
odbory vzdelávania
46 Matematika a štatistika 4610 Matematika
4620 Štatistika
48 Informatika, používanie počítačov 4810 Počítačové vedy
4820 Používanie počítačov
5 Technika,
výroba a
52 Technika a technické odbory 5200 Technika a technické odbory – širšie
zameranie programov
stavebníctvo 5210 Strojárstvo, kovovýroba a metalurgia
5220 Elektrotechnika a energetika
5230 Elektronika a automatizácia
5240 Chemické výroby
5250 Motorové vozidlá, lode a lietadlá
54 Výroba a spracovanie 5400 Výroba a spracovanie – širšie programy
5410 Potravinárstvo
5420 Výroba textilu, odevov a obuvi a
spracovanie kože
5430 Materiály (drevo, papier, plasty, sklo)
5440 Baníctvo a ťažba
58 Architektúra a stavebníctvo 5810 Architektúra a urbanizmus
5820 Stavebníctvo
6 Poľnohospo-
dárstvo a
62 Poľnohospodárstvo, lesníctvo a
rybolov
6200 Poľnohospodárstvo, lesníctvo a rybolov
– širšie programy
veterinárstvo 6210 Rastlinná a živočíšna výroba
6220 Záhradníctvo
6230 Lesníctvo
6240 Rybolov
64 Veterinárstvo 6410 Veterinárstvo
7 Zdravotníctvo 72 Zdravotníctvo 7200 Zdravotníctvo – širšie programy
a sociálna 7210 Humánna medicína
starostlivosť 7230 Ošetrovateľstvo
7240 Stomatológia
7250 Lekárska diagnostika a liečebná technika
7260 Terapia a rehabilitácia
7270 Farmácia
76 Sociálna starostlivosť 7610 Starostlivosť o deti a mládež
7620 Sociálna práca a poradenstvo
8 Služby 81 Osobné služby 8100 Osobné služby
8110 Hotely, reštaurácie a stravovanie
8120 Cestovný ruch, turistika, voľný čas
8130 Šport
8140 Služby pre domácnosť
8150 Kaderníctvo a kozmetika
84 Doprava a spoje 8400 Dopravné služby
85 Ochrana životného prostredia 8500 Ochrana životného prostredia – širšie
programy
8510 Technológia ochrany životného
prostredia
8520 Prírodné prostredie a prirodzené formy
života
8530 Verejné hygienické služby
86 Bezpečnostné služby 8600 Bezpečnostné služby – širšie programy
8610 Ochrana osôb a majetku
8620 Bezpečnosť a ochrana zdravia pri práci
8630 Vojsko a obrana
Neznáme 9999 Neznáme
"""

# pattern pre 4 cisla a to co je za tym nazov
pattern = r'^(\d{4})\s(.+)$'
matches = re.findall(pattern, obsah_vzdelávania, re.MULTILINE)

# Vytvor databazy
data_okresy = pd.DataFrame(data_okresy)
data_kraje = pd.DataFrame(data_kraje)
rezort = pd.DataFrame(rezort)
pravna_forma = pd.DataFrame(pravna_forma)
VI = pd.DataFrame(VI)
vlastnictvo = pd.DataFrame(vlastnictvo)
obsah_vzdelavania = pd.DataFrame(matches, columns=['Číselný kód', 'Názov'])

#drobne upravy kvoli mergovaniu
obsah_vzdelavania['Číselný kód'] = obsah_vzdelavania['Číselný kód'].astype('float64')
data_VI = data_VI.dropna(subset=['Vlastníctvo'])

#Zmerguj databazy
merged_vlastnictvo = pd.merge(vlastnictvo, data_VI, how='left', left_on='Číselný kód', right_on='Vlastníctvo')
merged_typ = pd.merge(VI, data_VI, how='left', left_on='Číselný kód', right_on='Typ')
merged_data_mapa = pd.merge(data_okresy, data_VI, how='left', left_on='Číselný kód', right_on='okres')
merged_data_zdroje = pd.merge(data_kraje, data_VA, how='left', left_on='Číselný kód', right_on='Kraj')
merged_data_obsah_vzdelavania = pd.merge(obsah_vzdelavania, data_VA, how='left', left_on='Číselný kód', right_on='Obsah vzdelávania')

# Kontingecne tabulky
pivot_table_mapa = merged_data_mapa.pivot_table(
    index='Úplný názov',  
    values='id', 
    aggfunc='count' 
)

pivot_table_zdroje = merged_data_zdroje.pivot_table(
    index='Úplný názov',
    values=['financovanie spolu', 'verejný sektor spolu'],
    aggfunc='sum'
)

pivot_table_typ = merged_typ.pivot_table(
    index='Typ',
    values=['financovanie spolu', 'verejný sektor spolu', 'Názov'],
    aggfunc={'financovanie spolu': 'sum', 'verejný sektor spolu': 'sum', 'Názov': 'first'}
)


pivot_table_vlastnictvo = merged_vlastnictvo.pivot_table(
    index='Vlastníctvo',
    values=['id', 'Názov'],
    aggfunc={'id': 'count', 'Názov': 'first'}
)

pivot_table_obsah_vzdelavania = merged_data_obsah_vzdelavania.pivot_table(
    index='Obsah vzdelávania',
    values=['id', 'Názov'],
    aggfunc={'id': 'count', 'Názov': 'first'}
)

pivot_table_pocet_VI = merged_data_zdroje.pivot_table(
    index='Úplný názov',
    values='id',
    aggfunc='count'
)

#zresetuj index kvoli uprave
pivot_table_mapa_reset = pivot_table_mapa.reset_index()
pivot_table_zdroje_reset = pivot_table_zdroje.reset_index()
pivot_table_typ_reset = pivot_table_typ.reset_index()
pivot_table_pocet_VI_reset = pivot_table_pocet_VI.reset_index()
pivot_table_vlastnictvo_reset = pivot_table_vlastnictvo.reset_index()
pivot_table_obsah_vzdelavania_reset = pivot_table_obsah_vzdelavania.reset_index()

#premenuj stlpce
pivot_table_zdroje_reset.rename(columns={'verejný sektor spolu': 'verejný sektor'}, inplace=True)
pivot_table_typ_reset.rename(columns={'verejný sektor spolu': 'verejný sektor'}, inplace=True)
pivot_table_pocet_VI_reset.rename(columns={'id': 'počet'}, inplace=True)
pivot_table_vlastnictvo_reset.rename(columns={'id': 'počet'}, inplace=True)
pivot_table_obsah_vzdelavania_reset.rename(columns={'id': 'počet'}, inplace=True)

pivot_table_vlastnictvo_reset["Vlastníctvo"] = pivot_table_vlastnictvo_reset["Vlastníctvo"].astype(str)


#Vypocitaj pre sukromny sektor financie
pivot_table_zdroje_reset['súkromný sektor'] = pivot_table_zdroje_reset['financovanie spolu'] - pivot_table_zdroje_reset['verejný sektor']
pivot_table_typ_reset['súkromný sektor'] = pivot_table_typ_reset['financovanie spolu'] - pivot_table_typ_reset['verejný sektor']

#Funkcia na formatovanie cisiel
def format_numbers(x):
    if isinstance(x, (int, float)):
        return "{:,.0f}".format(x)
    return x


# Zacni
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Odtiene modrej
blue_colors = ['#68AAD9', '#93CCEA', '#144B7B', '#BFEFFF', '#2269A3', '#3C88C5', '#93CCEA', '#144B7B', '#BFEFFF', '#68AAD9', '#3C88C5', '#2269A3']

#Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Ďalšie vzdelávanie vizuálne", className="text-center text-white py-2"), #nadpis

            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(  ###prave dropdown okno
                        id='chart-dropdown',
                        options=[
                            {'label': 'Zdroje financovania ďalšieho vzdelávania podľa krajov SR', 'value': 'blue'},
                            {'label': 'Zdroje financovania ďalšieho vzdelávania podľa organizácie', 'value': 'green'},
                            {'label': 'Počet vzdelávacích subjektov podľa krajov SR', 'value': 'red'},
                            {'label': 'Počet realizovaných vzdelávacích aktivít podľa obsahu vzdelávania', 'value': 'scatter_plot'},
                            {'label': 'Vzdelávacie subjekty podľa vlastníctva', 'value': 'orange'}
                        ],
                        value='blue',
                        clearable=False,
                        style={'width': '100%'},  # Adjust width
                        className='my-dropdown-style'  # pre styling dropdown okna
                    ),
                ], width=6),

                dbc.Col([
                    dcc.Dropdown(   ###lave dropdown okno
                        id='sector-dropdown',
                        options=[
                            {'label': 'Spolu', 'value': 'financovanie spolu'},
                            {'label': 'Súkromný sektor', 'value': 'súkromný sektor'},
                            {'label': 'Verejný sektor', 'value': 'verejný sektor'}
                        ],
                        value='financovanie spolu',
                        clearable=False,
                        style={'width': '100%'}, 
                        className='my-dropdown-style'
                    ),
                ], width=6),
            ]),

            dcc.Graph(id='chart-container', style={'height': 'calc(100vh - 80px)'})
        ], width=12, style={'height': '100vh'})
    ])
], fluid=True, style={'backgroundColor': 'black', 'height': '100vh', 'margin': '0'})



@app.callback(
    [Output('chart-container', 'figure'), Output('sector-dropdown', 'style')],
    [Input('chart-dropdown', 'value'), Input('sector-dropdown', 'value')]
)
def update_chart(selected_chart, selected_sector):
    fig = go.Figure()

    if selected_chart == 'blue':
        data_source = pivot_table_zdroje_reset
        y_axis_label = 'Úplný názov'
        colors = ['#3277CA', '#5B9BD5', '#80CBED']

        for filter_option in ['financovanie spolu', 'verejný sektor', 'súkromný sektor']: ##filtrovacie moznosti
            if filter_option in data_source.columns:
                data = data_source.sort_values(by=filter_option, ascending=False)
                fig.add_trace(go.Bar(
                    x=data[filter_option],
                    y=data[y_axis_label],
                    orientation='h',
                    name=filter_option,
                    hovertemplate='%{x:,.0f}',
                    marker=dict(color=colors.pop(0))
                ))

        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
        )

        fig.update_yaxes(title='', categoryorder='total ascending')
        fig.update_xaxes(
            title='',
            showgrid=False,
            tickfont=dict(color='white'),
        )

    elif selected_chart == 'green':
        # Ukaz dropdown menu pre tento typ
        sector_dropdown_style = {'display': 'block'}

        data_source = pivot_table_typ_reset

        fig = go.Figure(go.Treemap(
            labels=[f"<span style='font-size: 200%;'>{data_source['Názov'][index]}</span> - <b><span style='font-size: 200%;'>{value:,.0f} €</span></b>" for index, value in enumerate(data_source[selected_sector])],
            parents=[""] * len(data_source),
            values=data_source[selected_sector],
            textinfo="label",
            marker=dict(colors=blue_colors)  
        ))

        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
        )

        return fig, sector_dropdown_style


    elif selected_chart == 'red':
        data_source = pivot_table_pocet_VI_reset
        y_axis_label = 'Úplný názov'
        colors = ['#68AAD9', '#3C88C5', '#2269A3', '#144B7B', '#0C3366', '#082450', '#051A3D', '#03112D']
        
        data = data_source.sort_values(by='počet', ascending=False)
        fig.add_trace(go.Bar(
            x=data['počet'],
            y=data[y_axis_label],
            orientation='h',
            name='počet',
            hovertemplate='%{x:,.0f}',
            marker=dict(color=colors)
        ))

        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
        )

        fig.update_yaxes(title='', categoryorder='total ascending')
        fig.update_xaxes(
            title='',
            showgrid=False,
            tickfont=dict(color='white'),
        )

        
        
        
        
    elif selected_chart == 'scatter_plot':
        data_source = pivot_table_obsah_vzdelavania_reset

        if "Názov" in data_source and "počet" in data_source:

            fig = go.Figure(data=go.Scatter(
                x=data_source["Obsah vzdelávania"],
                y=data_source["počet"],
                mode='markers',
                marker=dict(color='blue'),
                hovertemplate='<br>Počet: %{y} <br>Názov: %{text}', 
                text=data_source["Názov"]  
            ))

            fig.update_layout(
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='white',
                showlegend=False,
                xaxis=dict( ##Schovaj x a y legendy
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False
                ),
                xaxis_title="",
                yaxis_title=""
            )

            # Zorad databazu a zober prvych 5
            top_five = data_source.nlargest(5, 'počet')

            # Zobraz permanentne pocet
            for _, row in top_five.iterrows():
                fig.add_annotation(
                    x=row['Obsah vzdelávania'],
                    y=row['počet'],
                    text=str(int(row['počet'])),
                    showarrow=True,
                    arrowhead=1,
                    ax=-40,
                    ay=0,
                    font=dict(
                        color='white',
                        size=12
                    )
                )
        else:
            print("Required columns not found in the data source")

        
    elif selected_chart == 'orange':
        data_source = pivot_table_vlastnictvo_reset
        y_axis_label = 'Názov'
        x_axis_data = 'počet'
        colors = ['#68AAD9', '#3C88C5', '#2269A3', '#144B7B', '#0C3366', '#082450', '#051A3D', '#03112D']

        data = data_source.sort_values(by=x_axis_data, ascending=False)
        fig.add_trace(go.Bar(
            x=data[x_axis_data],
            y=data[y_axis_label],
            orientation='h',
            name='počet',
            hovertemplate='%{x:,.0f}',
            marker=dict(color=colors)
        ))

        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
        )

        fig.update_yaxes(title='', categoryorder='total ascending')
        fig.update_xaxes(
            title='',
            showgrid=False,
            tickfont=dict(color='white'),
        )


    return fig, {'display': 'none'} if selected_chart != 'green' else {'display': 'block'}

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050, dev_tools_ui=False)