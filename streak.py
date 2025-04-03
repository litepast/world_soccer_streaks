# https://www.kaggle.com/datasets/patateriedata/all-international-football-results/code
"""
   Creates streaks data from kaggle dataset
"""
from datetime import datetime
from zoneinfo import ZoneInfo

class Streak:
    """
    Class in charge of the pipeline transforming the dataset to a comprehensive json
    """
    def __init__(self, matches, countries):
        self.matches = matches
        self.countries = countries
        self._minimum_total = 10
        self._top_streaks = 20
        self.streaks = {}
        self.unbeaten_streaks = {}
        self.winless_streaks = {}
        self.winning_streaks = {}
        self.losing_streaks = {}
        self.drawing_streaks = {}
        self.active_streaks = {}
        self.alltime_streaks = {}


    def __get_current_country(self,country):
        """
            Checks if a country team still exists today or has been succeded    
        """
        return True if country in self.countries else False

    def __get_match_result(self, home_score, away_score, home_team, away_team):
        """
            Returns which countries won or lost a match, of if it was a draw   
        """
        if home_score > away_score:
            return False, home_team, away_team
        elif home_score < away_score:
            return False, away_team, home_team
        else:
            return True, None, None

    def __get_streak_condition(self,team, streaks):
        """
            Checks is the result starts or not a streak  
        """
        if team not in streaks or streaks[team][-1]['details_end']:
            return False #new streak needed, either for new or existing team
        else:
            return True #the streak is still running

    def __get_unfinished_streaks(self, all_streaks):
        """
            Returns the unfinished streaks for current countries  
        """
        return   [
            {"country": count, "current": self.__get_current_country(count), **streak}
            for count, streaks in all_streaks.items()
            for streak in streaks if streak["details_end"] == {}
        ]

    def __filter_by_min(self, minimum_streak, filtered_streak):
        """
            Returns and filters streaks where the total is bigger than the minimum value  
        """
        return [
            {"country": count, "current": self.__get_current_country(count), **streak}
            for count, streaks in filtered_streak.items()
            for streak in streaks if streak["total"] >= minimum_streak
        ]

    def __filter_by_top(self, top_streaks, streaks):
        """
            Returns and top streaks by total
        """
        if len(streaks) > top_streaks:
            smallest_total = streaks[top_streaks-1]["total"]
            return [x for x in  streaks if x["total"] >= smallest_total ]
        else:
            return streaks

    def __filter_by_current_country(self, streak):
        """
            Filters streaks if they are by a current country
        """
        return [x for x in streak if x["current"]]

    def get_alltime_top_streaks(self):
        """ Tracks all types of streaks """

        streak_types = {
                    "unbeaten": self.unbeaten_streaks,
                    "winless": self.winless_streaks,
                    "winning": self.winning_streaks,
                    "losing": self.losing_streaks,
                    "drawing": self.drawing_streaks
        }

        for row in self.matches.itertuples(index=False):
            date, home_team, away_team, home_score, away_score, tournament, host = \
                row.date, row.home_team, row.away_team, row.home_score, row.away_score, \
                row.tournament, row.country

            match_detail = {"date": date, "home_team": home_team, "away_team": away_team,
                            "home_score": home_score, "away_score": away_score,
                            "tournament": tournament, "host": host}             
            is_draw, winner, loser = self.__get_match_result(home_score, away_score,
                                                             home_team, away_team)

            for team in [home_team, away_team]:
                is_winner = team == winner
                is_loser = team == loser

                # Each streak finish condition
                update_conditions = {
                    "unbeaten": not is_loser,
                    "winless": not is_winner,
                    "winning": is_winner,
                    "losing": is_loser,
                    "drawing": is_draw
                }

                for streak_name, streak_dict in streak_types.items():
                    streak_ended = self.__get_streak_condition(team, streak_dict)

                    if not update_conditions[streak_name]:  # Streak is broken
                        if streak_ended:
                            streak_dict[team][-1]["details_end"] = match_detail
                    else:
                        if not streak_ended:
                            streak_dict.setdefault(team, []).append(
                                {"total": 0, "wins": 0, "draws": 0, "losses": 0,
                                 "date_started": date,
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

        unbeaten_streaks = self.__filter_by_min(self._minimum_total, streak_types["unbeaten"])
        unbeaten_streaks.sort(key=lambda x: ((x['total']), x['wins']), reverse=True)
        winning_streaks = self.__filter_by_min(self._minimum_total, streak_types["winning"])
        winning_streaks.sort(key=lambda x: x['total'], reverse=True)
        losing_streaks = self.__filter_by_min(self._minimum_total, streak_types["losing"])
        losing_streaks.sort(key=lambda x: x['total'], reverse=True)
        winless_streaks = self.__filter_by_min(self._minimum_total, streak_types["winless"])
        winless_streaks.sort(key=lambda x: ((x['total']), x['losses']), reverse=True)
        drawing_streaks = self.__filter_by_min(6, streak_types["drawing"])
        drawing_streaks.sort(key=lambda x: x['total'], reverse=True)

        self.alltime_streaks["Unbeaten"] = self.__filter_by_top(self._top_streaks, unbeaten_streaks)
        self.alltime_streaks["Winning"] = self.__filter_by_top(self._top_streaks, winning_streaks)
        self.alltime_streaks["Losing"] = self.__filter_by_top(self._top_streaks, losing_streaks)
        self.alltime_streaks["Winless"] = self.__filter_by_top(self._top_streaks, winless_streaks)
        self.alltime_streaks["Drawing"] = self.__filter_by_top(self._top_streaks, drawing_streaks)
        return self.alltime_streaks

    def get_active_top_streaks(self):
        """ Returns top 5 ongoing streaks by current countries"""
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

        self.active_streaks["Unbeaten"] = self.__filter_by_top(min_active, active_unbeaten)
        self.active_streaks["Winning"] = self.__filter_by_top(min_active, active_winning)
        self.active_streaks["Losing"] = self.__filter_by_top(min_active, active_losing)
        self.active_streaks["Winless"] = self.__filter_by_top(min_active, active_winless)
        self.active_streaks["Drawing"] = self.__filter_by_top(min_active, active_drawing)

        return self.active_streaks

    def get_all_top_streaks(self):
        """ Returns top all time and ongoing streaks"""
        dt_update = datetime.now(ZoneInfo("America/Mexico_City"))
        dt_update_str = dt_update.isoformat()
        self.streaks['date_updated'] = dt_update_str
        self.streaks['all_time'] = self.get_alltime_top_streaks()
        self.streaks['active'] = self.get_active_top_streaks()
        return self.streaks
        