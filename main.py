import scrap

estadisticas = []
for year in range(2018,2010,-1):
    html = scrap.download_html("http://www.atpworldtour.com/en/scores/results-archive?year="+str(year))
    if html != "":
        urls_primera_parte = scrap.lookfor_html(html,'td')
        urls_segunda_parte = scrap.get_first_part(urls_primera_parte)
        for i in range(len(urls_segunda_parte)):
            #html = scrap.download_html("http://www.atpworldtour.com/en/scores/archive/rio-de-janeiro/96/2016/results")
            html = scrap.download_html("http://www.atpworldtour.com"+urls_segunda_parte[
                divmod(-i-1, len(urls_segunda_parte))[1]])
            fecha_torneo = scrap.get_date_tournament(html)
            torneo = scrap.get_tournament(html)
            superficie = scrap.get_surface(html)
            if torneo != "":
                partidos = scrap.get_url_matches(html)
                for partido in partidos:
                    estadistica = scrap.get_statist_match("http://www.atpworldtour.com"+partido, torneo, fecha_torneo,
                                                          superficie)
                    if len(estadistica[0]) != 0:
                        estadisticas.append(estadistica)
            else:
                print "http://www.atpworldtour.com"+urls_segunda_parte[divmod(-i-1, len(urls_segunda_parte))[1]]
    print "Scraped year " + str(year)
scrap.write_xls(estadisticas)

