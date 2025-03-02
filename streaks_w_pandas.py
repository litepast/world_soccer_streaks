# https://www.kaggle.com/datasets/patateriedata/all-international-football-results/code

class Streak:
    """
 
    """
    def __init__(self, matches, countries):
        self.matches = matches
        self.countries = countries
        self.unbeaten_streaks = {}
        self.winless_streaks = {}
        self.winning_streaks = {}
        self.losing_streaks = {}
        self.drawing_streaks = {}
        self.top_active_streaks = {}
        self.top_alltime_streaks = {}
        self._minimum_total = 10
        self._top_streaks = 20

    def __get_current_country(self,country):
        return  True if country in self.countries else False
    
    def __get_match_result(self, home_score, away_score, home_team, away_team):            
        if home_score > away_score:
            return False, home_team, away_team
        elif home_score < away_score:
            return False, away_team, home_team
        else:
            return True, None, None

    def __get_addition_condition(self,team, streaks):        
        if team not in streaks:
            return 1 #if the team is not on the streaks data at all
        elif streaks[team][-1]['details_end']:
            return 2 #team had its last streak finished
        else:
            return 3 #the streak is still running
        
    def __get_unfinished_streaks(self, all_streaks):
        return   [
            {"country": count, "current": self.__get_current_country(count), **streak}
            for count, streaks in all_streaks.items()
            for streak in streaks if streak["details_end"] == {} 
        ]
            
    def __filter_by_country(self, country, streaks):
        if country:
            country_streak={}
            country_streak[country] = streaks[country]
            return country_streak
        else:
            return streaks
        #         if country:
        #     return {country: streaks.get(country, [])}
        # return streaks
    
    def __filter_by_minimum(self, minimum_streak, filtered_streak):
        return [
            {"country": count, "current": self.__get_current_country(count), **streak}
            for count, streaks in filtered_streak.items()
            for streak in streaks if streak["total"] >= minimum_streak
        ]
    
    def __filter_by_top(self, top_streaks, streaks):
        if len(streaks) > top_streaks:
            smallest_total = streaks[top_streaks-1]["total"]
            #print('least total',smallest_total)
            return [x for x in  streaks if x["total"] >= smallest_total ]
        else:
            return streaks
        
    def __filter_by_current_country(self, streak):
       return [x for x in streak if x["current"]]
            
    def get_unbeaten_streaks(self, minumum_streak=None, top_streaks=None, country=None):
        minumum_streak = self._minimum_total if minumum_streak is None else minumum_streak
        top_streaks = self._top_streaks if top_streaks is None else top_streaks
        matches = self.matches 
        matches = self.matches.query("home_team == @country or away_team == @country") if country else self.matches
        
        for row in matches.itertuples(index=False):
            date, home_team, away_team, home_score, away_score, tournament, host = \
                row.date, row.home_team, row.away_team, row.home_score, row.away_score, row.tournament, row.country
            match_detail = { 
                "date": date, 
                "home_team": home_team, "away_team": away_team,
                "home_score": home_score, "away_score": away_score,
                "tournament": tournament, "host": host        
            }

            draw, winner, loser = self.__get_match_result(home_score, away_score, home_team, away_team)   
            
            for team in [home_team, away_team]:  
                add_condition = self.__get_addition_condition(team, self.unbeaten_streaks)  
                if team == loser:
                    if add_condition == 3: #if loser had active streak, it will be marked as finished
                        self.unbeaten_streaks[team][-1]["details_end"] = match_detail  
                else:
                    if add_condition in [1, 2]:
                        self.unbeaten_streaks.setdefault(team, []).append(
                            {"total": 0, "wins": 0, "draws": 0, "losses": 0, "date_started": date,
                             "details_streak": [], "details_end": {}}
                        )
                    streak_to_update = self.unbeaten_streaks[team][-1]
                    streak_to_update["total"] += 1
                    streak_to_update["wins" if team == winner else "draws"] += 1
                    streak_to_update["details_streak"].append(match_detail)

        streaks_filtered_by_country = self.__filter_by_country(country, self.unbeaten_streaks)
        streaks_filtered_by_min = self.__filter_by_minimum(minumum_streak, streaks_filtered_by_country)
        streaks_filtered_by_min.sort(key=lambda x: ((x['total']), x['wins']), reverse=True)
        return self.__filter_by_top(top_streaks, streaks_filtered_by_min )

    def get_winless_streaks(self, minimum_streak=None, top_streaks=None, country=None):
        """ Tracks longest winless streaks (draws + losses) """
        minimum_streak = self._minimum_total if minimum_streak is None else minimum_streak
        top_streaks = self._top_streaks if top_streaks is None else top_streaks
        matches = self.matches.query("home_team == @country or away_team == @country") if country else self.matches

        for row in matches.itertuples(index=False):
            date, home_team, away_team, home_score, away_score, tournament, host = \
                row.date, row.home_team, row.away_team, row.home_score, row.away_score, row.tournament, row.country
            
            match_detail = {"date": date, "home_team": home_team, "away_team": away_team,
                            "home_score": home_score, "away_score": away_score,
                            "tournament": tournament, "host": host}

            draw, winner, loser = self.__get_match_result(home_score, away_score, home_team, away_team)

            for team in [home_team, away_team]:  
                add_condition = self.__get_addition_condition(team, self.winless_streaks)
                
                if team == winner:
                    if add_condition == 3:
                        self.winless_streaks[team][-1]["details_end"] = match_detail
                else:
                    if add_condition in [1, 2]:
                        self.winless_streaks.setdefault(team, []).append(
                            {"total": 0, "wins": 0, "draws": 0, "losses": 0, "date_started": date,
                             "details_streak": [], "details_end": {}}
                        )
                    streak_to_update = self.winless_streaks[team][-1]
                    streak_to_update["total"] += 1
                    streak_to_update["draws" if draw else "losses"] += 1
                    streak_to_update["details_streak"].append(match_detail)

        streaks_filtered_by_country = self.__filter_by_country(country, self.winless_streaks)
        streaks_filtered_by_min = self.__filter_by_minimum(minimum_streak, streaks_filtered_by_country)
        streaks_filtered_by_min.sort(key=lambda x: x['total'], reverse=True)
        return self.__filter_by_top(top_streaks, streaks_filtered_by_min)

    def get_winning_streaks(self, minimum_streak=None, top_streaks=None, country=None):
        """ Tracks longest winning streaks (draws + losses) """
        minimum_streak = self._minimum_total if minimum_streak is None else minimum_streak
        top_streaks = self._top_streaks if top_streaks is None else top_streaks
        matches = self.matches.query("home_team == @country or away_team == @country") if country else self.matches

        for row in matches.itertuples(index=False):
            date, home_team, away_team, home_score, away_score, tournament, host = \
                row.date, row.home_team, row.away_team, row.home_score, row.away_score, row.tournament, row.country
            
            match_detail = {"date": date, "home_team": home_team, "away_team": away_team,
                            "home_score": home_score, "away_score": away_score,
                            "tournament": tournament, "host": host}

            draw, winner, loser = self.__get_match_result(home_score, away_score, home_team, away_team)

            for team in [home_team, away_team]:  
                add_condition = self.__get_addition_condition(team, self.winning_streaks)
                
                if team != winner:
                    if add_condition == 3:
                        self.winning_streaks[team][-1]["details_end"] = match_detail
                else:
                    if add_condition in [1, 2]:
                        self.winning_streaks.setdefault(team, []).append(
                            {"total": 0, "wins": 0, "draws": 0, "losses": 0, "date_started": date,
                             "details_streak": [], "details_end": {}}
                        )
                    streak_to_update = self.winning_streaks[team][-1]
                    streak_to_update["total"] += 1
                    streak_to_update["wins"] += 1
                    streak_to_update["details_streak"].append(match_detail)

        streaks_filtered_by_country = self.__filter_by_country(country, self.winning_streaks)
        streaks_filtered_by_min = self.__filter_by_minimum(minimum_streak, streaks_filtered_by_country)
        streaks_filtered_by_min.sort(key=lambda x: x['total'], reverse=True)
        return self.__filter_by_top(top_streaks, streaks_filtered_by_min)
    
    def get_losing_streaks(self, minimum_streak=None, top_streaks=None, country=None):
        """ Tracks longest winning streaks (draws + losses) """
        minimum_streak = self._minimum_total if minimum_streak is None else minimum_streak
        top_streaks = self._top_streaks if top_streaks is None else top_streaks
        matches = self.matches.query("home_team == @country or away_team == @country") if country else self.matches

        for row in matches.itertuples(index=False):
            date, home_team, away_team, home_score, away_score, tournament, host = \
                row.date, row.home_team, row.away_team, row.home_score, row.away_score, row.tournament, row.country
            
            match_detail = {"date": date, "home_team": home_team, "away_team": away_team,
                            "home_score": home_score, "away_score": away_score,
                            "tournament": tournament, "host": host}

            draw, winner, loser = self.__get_match_result(home_score, away_score, home_team, away_team)

            for team in [home_team, away_team]:  
                add_condition = self.__get_addition_condition(team, self.losing_streaks)
                
                if team != loser:
                    if add_condition == 3:
                        self.losing_streaks[team][-1]["details_end"] = match_detail
                else:
                    if add_condition in [1, 2]:
                        self.losing_streaks.setdefault(team, []).append(
                            {"total": 0, "wins": 0, "draws": 0, "losses": 0, "date_started": date,
                             "details_streak": [], "details_end": {}}
                        )
                    streak_to_update = self.losing_streaks[team][-1]
                    streak_to_update["total"] += 1
                    streak_to_update["losses"] += 1
                    streak_to_update["details_streak"].append(match_detail)

        streaks_filtered_by_country = self.__filter_by_country(country, self.losing_streaks)
        streaks_filtered_by_min = self.__filter_by_minimum(minimum_streak, streaks_filtered_by_country)
        streaks_filtered_by_min.sort(key=lambda x: x['total'], reverse=True)
        return self.__filter_by_top(top_streaks, streaks_filtered_by_min)

    def get_drawing_streaks(self, minimum_streak=None, top_streaks=None, country=None):
        """ Tracks longest wtie streaks (draws + losses) """
        minimum_streak = self._minimum_total if minimum_streak is None else minimum_streak
        top_streaks = self._top_streaks if top_streaks is None else top_streaks
        matches = self.matches.query("home_team == @country or away_team == @country") if country else self.matches

        for row in matches.itertuples(index=False):
            date, home_team, away_team, home_score, away_score, tournament, host = \
                row.date, row.home_team, row.away_team, row.home_score, row.away_score, row.tournament, row.country
            
            match_detail = {"date": date, "home_team": home_team, "away_team": away_team,
                            "home_score": home_score, "away_score": away_score,
                            "tournament": tournament, "host": host}

            draw, winner, loser = self.__get_match_result(home_score, away_score, home_team, away_team)

            for team in [home_team, away_team]:  
                add_condition = self.__get_addition_condition(team, self.drawing_streaks)
                
                if not draw:
                    if add_condition == 3:
                        self.drawing_streaks[team][-1]["details_end"] = match_detail
                else:
                    
                    if add_condition in [1, 2]:
                        self.drawing_streaks.setdefault(team, []).append(
                            {"total": 0, "wins": 0, "draws": 0, "losses": 0, "date_started": date,
                             "details_streak": [], "details_end": {}}
                        )
                    streak_to_update = self.drawing_streaks[team][-1]
                    streak_to_update["total"] += 1
                    streak_to_update["draws"] += 1
                    streak_to_update["details_streak"].append(match_detail)

        streaks_filtered_by_country = self.__filter_by_country(country, self.drawing_streaks)
        streaks_filtered_by_min = self.__filter_by_minimum(minimum_streak, streaks_filtered_by_country)
        streaks_filtered_by_min.sort(key=lambda x: x['total'], reverse=True)
        return self.__filter_by_top(top_streaks, streaks_filtered_by_min)

    def get_all_top_streaks(self):
        """ Tracks all types of streaks in one gom no filters """

        streak_types = {
                    "unbeaten": self.unbeaten_streaks,
                    "winless": self.winless_streaks,
                    "winning": self.winning_streaks,
                    "losing": self.losing_streaks,
                    "drawing": self.drawing_streaks
        }

        for row in self.matches.itertuples(index=False):
            date, home_team, away_team, home_score, away_score, tournament, host = \
                row.date, row.home_team, row.away_team, row.home_score, row.away_score, row.tournament, row.country
            
            match_detail = {"date": date, "home_team": home_team, "away_team": away_team,
                            "home_score": home_score, "away_score": away_score,
                            "tournament": tournament, "host": host}
        
            is_draw, winner, loser = self.__get_match_result(home_score, away_score, home_team, away_team)

            for team in [home_team, away_team]:  
                is_winner = team == winner
                is_loser = team == loser

                # Define how each streak type should be updated
                update_conditions = {
                    "unbeaten": not is_loser,
                    "winless": not is_winner,
                    "winning": is_winner,
                    "losing": is_loser,
                    "drawing": is_draw
                }

                for streak_name, streak_dict in streak_types.items():
                    add_condition = self.__get_addition_condition(team, streak_dict)

                    if not update_conditions[streak_name]:  # Streak is broken
                        if add_condition == 3:
                            streak_dict[team][-1]["details_end"] = match_detail
                    else:
                        if add_condition in [1, 2]:
                            streak_dict.setdefault(team, []).append(
                                {"total": 0, "wins": 0, "draws": 0, "losses": 0, "date_started": date,
                                "details_streak": [], "details_end": {}}
                            )
                        streak_to_update = streak_dict[team][-1]
                        streak_to_update["total"] += 1
                        if streak_name == "winning":
                            streak_to_update["wins"] += 1
                        elif streak_name == "losing":
                            streak_to_update["losses"] += 1
                        elif streak_name == "drawing":
                            streak_to_update["draws"] += 1
                        elif streak_name == "unbeaten":
                            streak_to_update["wins" if is_winner else "draws"] += 1
                        elif streak_name == "winless":
                            streak_to_update["draws" if is_draw else "losses"] += 1
                        streak_to_update["details_streak"].append(match_detail)

        final_unbeaten_streaks = self.__filter_by_minimum(self._minimum_total, streak_types["unbeaten"])
        final_unbeaten_streaks.sort(key=lambda x: ((x['total']), x['wins']), reverse=True)     
        final_winning_streaks = self.__filter_by_minimum(self._minimum_total, streak_types["winning"])
        final_winning_streaks.sort(key=lambda x: x['total'], reverse=True)  
        final_losing_streaks = self.__filter_by_minimum(self._minimum_total, streak_types["winning"])
        final_losing_streaks.sort(key=lambda x: x['total'], reverse=True)        
        final_winless_streaks = self.__filter_by_minimum(self._minimum_total, streak_types["winless"])
        final_winless_streaks.sort(key=lambda x: ((x['total']), x['losses']), reverse=True)   
        final_drawing_streaks = self.__filter_by_minimum(6, streak_types["drawing"])
        final_drawing_streaks.sort(key=lambda x: x['total'], reverse=True)

        self.top_alltime_streaks["unbeaten"] = self.__filter_by_top(self._top_streaks, final_unbeaten_streaks)
        self.top_alltime_streaks["winning"] = self.__filter_by_top(self._top_streaks, final_winning_streaks)
        self.top_alltime_streaks["losing"] = self.__filter_by_top(self._top_streaks, final_losing_streaks)
        self.top_alltime_streaks["winless"] = self.__filter_by_top(self._top_streaks, final_winless_streaks)
        self.top_alltime_streaks["drawing"] = self.__filter_by_top(self._top_streaks, final_drawing_streaks)
        
        return self.top_alltime_streaks

    def get_all_active_streaks(self):
        min_active = 5

        active_unbeaten = self.__get_unfinished_streaks(self.unbeaten_streaks)     
        active_unbeaten = self.__filter_by_current_country(active_unbeaten)
        active_unbeaten.sort(key=lambda x: ((x['total']), x['wins'], x['draws']), reverse=True)

        active_winning = self.__get_unfinished_streaks(self.winning_streaks)     
        active_winning = self.__filter_by_current_country(active_winning)
        active_winning.sort(key=lambda x: x['total'], reverse=True)

        active_losing = self.__get_unfinished_streaks(self.losing_streaks)     
        active_losing = self.__filter_by_current_country(active_losing)
        active_losing.sort(key=lambda x: x['total'], reverse=True)

        active_winless = self.__get_unfinished_streaks(self.winless_streaks)     
        active_winless = self.__filter_by_current_country(active_winless)
        active_winless.sort(key=lambda x: ((x['total']), x['losses'],x['draws']), reverse=True)

        active_drawing = self.__get_unfinished_streaks(self.drawing_streaks)     
        active_drawing = self.__filter_by_current_country(active_drawing)
        active_drawing.sort(key=lambda x: x['total'], reverse=True)

        self.top_active_streaks["unbeaten"] = self.__filter_by_top(min_active, active_unbeaten)
        self.top_active_streaks["winning"] = self.__filter_by_top(min_active, active_winning)
        self.top_active_streaks["losing"] = self.__filter_by_top(min_active, active_losing)
        self.top_active_streaks["winless"] = self.__filter_by_top(min_active, active_winless)
        self.top_active_streaks["drawing"] = self.__filter_by_top(min_active, active_drawing)

        return self.top_active_streaks
