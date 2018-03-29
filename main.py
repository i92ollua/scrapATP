import scrap

estadisticas = []
for year in range(2018,2019):
    html = scrap.download_html("http://www.atpworldtour.com/en/scores/results-archive?year="+str(year))
    urls_primera_parte = scrap.lookfor_html(html,'td')
    urls_segunda_parte = scrap.get_first_part(urls_primera_parte)
    torneos = scrap.get_tournaments(urls_primera_parte)
    for i in int(len(torneos)):
        html = scrap.download_html("http://www.atpworldtour.com"+urls_segunda_parte[-i])
        fecha_torneo = scrap.get_date_tournament(html)
        partidos = scrap.get_url_matches(html)
        for partido in partidos:
            estadistica = scrap.get_statist_match("http://www.atpworldtour.com"+partido,
                                                  torneos[-i],fecha_torneo)
            if len(estadistica[0])!= 0:
                estadisticas.append(estadistica)
scrap.write_xls(estadisticas)
print estadisticas

