import scrap

estadisticas = []
for year in range(2019,2010,-1):
    html = scrap.download_html("http://www.atpworldtour.com/en/scores/results-archive?year="+str(year))
    if html != "":
        urls_primera_parte = scrap.lookfor_html(html,'td')
        urls_segunda_parte = scrap.get_first_part(urls_primera_parte)
        torneos = scrap.get_tournaments(urls_primera_parte)
        superficies = scrap.get_tournaments_surface(html)
        for i in range(len(urls_segunda_parte)):
            html = scrap.download_html("http://www.atpworldtour.com"+urls_segunda_parte[
                divmod(-i-1, len(urls_segunda_parte))[1]])
            if html != "":
                fecha_torneo = scrap.get_date_tournament(html)
                partidos = scrap.get_url_matches(html)
                for partido in partidos:
                    estadistica = scrap.get_statist_match("http://www.atpworldtour.com"+partido,
                                                          torneos[divmod(-i-1, len(urls_segunda_parte))[1]], fecha_torneo,
                                                          superficies[divmod(-i - 1, len(urls_segunda_parte))[1]])
                    if len(estadistica[0]) != 0:
                        estadisticas.append(estadistica)
    print "Scraped year " + str(year)
scrap.write_xls(estadisticas)

