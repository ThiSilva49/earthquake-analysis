import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap

df = pd.read_csv('terremoto.csv')

m = folium.Map(location=[0, 0], zoom_start=2)
heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)
m.save('heatmap.html')


country_counts = df['Place'].value_counts().head(10)
fig = px.bar(country_counts, x=country_counts.index, y=country_counts.values,
             labels={'x': 'País/Região', 'y': 'Número de Terremotos'},
             title='Top 10 Países/Regiões com Mais Terremotos',
             color=country_counts.values,
             color_continuous_scale='Viridis')
fig.update_xaxes(tickangle=45)
fig.show()


fig = px.scatter(df, x='Longitude', y='Latitude', color='Mag',
                 title='Distribuição Geográfica dos Terremotos',
                 labels={'Longitude': 'Longitude', 'Latitude': 'Latitude'},
                 color_continuous_scale='Viridis')
fig.update_traces(marker=dict(size=5, opacity=0.5, line=dict(width=0)))
fig.show()


fig = px.histogram(df, x='Mag', nbins=30, title='Distribuição das Magnitudes dos Terremotos')
fig.update_xaxes(title='Magnitude')
fig.update_yaxes(title='Frequência')
fig.show()


fig = px.box(df.head(100), x='Place', y='Mag', title='Distribuição das Magnitudes por Região')
fig.update_xaxes(tickangle=45)
fig.show()




df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace=True)


df_resampled = df.resample('M').count()
fig = px.line(df_resampled, x=df_resampled.index, y='Mag',
              title='Frequência de Terremotos ao Longo do Tempo',
              labels={'Mag': 'Número de Terremotos', 'Time': 'Data'})
fig.show()


df['Year'] = df.index.year
df['Month'] = df.index.month
year_counts = df['Year'].value_counts().sort_index()
fig = px.bar(year_counts, x=year_counts.index, y=year_counts.values,
             labels={'x': 'Ano', 'y': 'Número de Terremotos'},
             title='Número de Terremotos por Ano',
             color=year_counts.values,
             color_continuous_scale='Viridis')
fig.show()


fig = px.scatter(df, x='Mag', y='Depth', title='Relação entre Magnitude e Profundidade dos Terremotos',
                 labels={'Mag': 'Magnitude', 'Depth': 'Profundidade (km)'})
fig.show()


top_earthquakes = df.nlargest(10, 'Mag').reset_index()
print(top_earthquakes[['Time', 'Place', 'Mag', 'Depth']])


fig = px.bar(top_earthquakes, x='Place', y='Mag', title='Top 10 Terremotos de Maior Magnitude',
             labels={'Place': 'Localização', 'Mag': 'Magnitude'},
             color='Mag', color_continuous_scale='Viridis')
fig.update_xaxes(tickangle=45)
fig.show()


if 'Type' in df.columns:
    fault_counts = df['Type'].value_counts()
    fig = px.pie(fault_counts, names=fault_counts.index, values=fault_counts.values,
                 title='Distribuição dos Tipos de Falha Geológica')
    fig.show()


if 'Energy' in df.columns:
    df['Energy'] = df['Energy'].fillna(0)  
    df_resampled_energy = df.resample('Y')['Energy'].sum()
    fig = px.area(df_resampled_energy, x=df_resampled_energy.index, y=df_resampled_energy.values,
                  title='Energia Total Liberada pelos Terremotos ao Longo do Tempo',
                  labels={'Energy': 'Energia Liberada', 'Time': 'Ano'})
    fig.show()
