import scrap


for year in range(2010,2018):
    html = scrap.download_html("http://www.atpworldtour.com/en/scores/results-archive?year="+str(year))
    urls_primera_parte = scrap.lookfor_html(html,'td')
    urls_segunda_parte = scrap.get_first_part(urls_primera_parte)
    torneos = scrap.get_tournaments(urls_primera_parte)
    for url,torneo in zip(urls_segunda_parte,torneos):
        html = scrap.download_html("http://www.atpworldtour.com"+url)
        fecha_torneo = scrap.get_date_tournament(html)
        partidos = scrap.get_url_matches(html)
        for partido in partidos:
            estadisticas = scrap.get_statist_match("http://www.atpworldtour.com"+partido)
    print urls_segunda_parte
print "Done"
