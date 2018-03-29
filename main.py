import scrap

estadisticas = []
for year in range(2019,2010,-1):
    html = scrap.download_html("http://www.atpworldtour.com/en/scores/results-archive?year="+str(year))
    urls_primera_parte = scrap.lookfor_html(html,'td')
    urls_segunda_parte = scrap.get_first_part(urls_primera_parte)
    torneos = scrap.get_tournaments(urls_primera_parte)
    for url,torneo in zip(urls_segunda_parte,torneos):
        html = scrap.download_html("http://www.atpworldtour.com"+url)
        fecha_torneo = scrap.get_date_tournament(html)
        partidos = scrap.get_url_matches(html)
        for i in len(partidos):
            estadistica = scrap.get_statist_match("http://www.atpworldtour.com"+partidos[-i], torneo[-i],fecha_torneo[-i])
            if len(estadistica[0])!= 0:
                estadisticas.append(estadistica)
    print("Year "+str(year)+" done")
scrap.write_xls(estadisticas)
print estadisticas

