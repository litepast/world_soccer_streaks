<template>
  <table>
    <thead>
      <tr class="top-header">
        <td class="side-col"></td>
        <td style="text-align: left;">Country</td>
        <td>Total</td>
        <td>Record (W-D-L)</td>
        <td>Date Started</td>
        <td>Date Ended</td>
        <td class="side-col"></td>
      </tr>
    </thead>
    <tbody>
      <template class="temp" v-for="(streak, i) in streaks">
        <tr class="streak" @click="showDetails[i] = !showDetails[i]">
          <td class="side-col"></td>
          <td style="display: flex; padding-left: 10px; align-items: center;">
            <div style="text-align: center; padding-right: 5px;">
              {{i+1}}
            </div>
            <div style="text-align: left; white-space: nowrap; overflow: hidden;text-overflow: ellipsis;" :title="streak.country">
              {{streak.country}}
            </div>              
          </td>
          <td>{{ streak.total }}</td>
          <td>{{ streak.wins }}-{{ streak.draws }}-{{ streak.losses }}</td>
          <td>{{ streak.date_started }}</td>
          <td>
            {{ streak.details_end.date ? streak.details_end.date: '-'}}            
          </td>
          <td class="side-col"></td>
        </tr>
        <tr class="details-header" v-show="showDetails[i]">
          <td class="side-col"></td>
          <td>Match Date</td>
          <td>Home Team</td>
          <td>Result</td>
          <td>Away Team</td>
          <td>Tournament</td>
          <td class="side-col"></td>
        </tr>
        <tr class="details" v-show="showDetails[i]" @click="showDetails[i] = !showDetails[i]" v-for="(detail, j) in streak.details_streak">
          <td class="side-col"></td>
          <td>{{ detail.date }}</td>
          <td :style="countryBold(streak.country, detail.home_team)">{{ detail.home_team }}</td>
          <td>{{ detail.home_score }} - {{ detail.away_score }}</td>
          <td :style="countryBold(streak.country, detail.away_team)">{{ detail.away_team }}</td>
          <td style="white-space: nowrap; overflow: hidden;text-overflow: ellipsis;" :title="detail.tournament">
            {{ detail.tournament }}
          </td>
          <td class="side-col"></td>
        </tr>

        <tr
          class="end-streak"
          v-if="showEnd"
          v-show="showDetails[i]"
          title="Match that ended the streak"
          @click="showDetails[i] = !showDetails[i]"
        >
        <td class="side-col"></td>
          <td>{{ streak.details_end.date }}</td>
          <td :style="countryBold(streak.country, streak.details_end.home_team)">
            {{ streak.details_end.home_team }}
          </td>
          <td>{{ streak.details_end.home_score }} - {{ streak.details_end.away_score }}</td>
          <td :style="countryBold(streak.country, streak.details_end.away_team)">
            {{ streak.details_end.away_team }}
          </td>
          <td :title="streak.details_end.tournament">
            {{ streak.details_end.tournament }}
          </td>
          <td class="side-col"></td>
        </tr>
      </template>
    </tbody>
  </table>
</template>

<script setup>
import { ref, defineProps, computed } from 'vue'
const showDetails = ref(Array(streaks.length).fill(false))

const { streaks, showEnd } = defineProps(['streaks', 'maxLen', 'showEnd'])

function countryBold(a, b) {
  if (a == b) {
    return 'font-weight: bold'
  }
}
</script>

<style scoped>

.top-header{
  font-size: smaller;
  color: rgb(160, 161, 175);
  background-color: rgb(16, 18, 24);
  border-bottom: 1px solid rgb(54, 58, 66);
}

.top-header td{
  padding-top: 10px;
  padding-bottom: 10px;
}

.side-col{
  width: 10px;   
  border-bottom: 1px solid rgb(16, 18, 24);
}

.streak {
  cursor: pointer;
  background-color: rgb(16, 18, 24);
  border-bottom: 1px solid rgb(54, 58, 66);
}

.streak td{
  padding-bottom: 5px;
  padding-top: 5px;
  
}

.streak:hover{
  background-color: rgb(48, 49, 52);
}

.details-header {
  font-size: small;
  background-color: rgb(2, 10, 40);
}

.details {
  font-size: small;
  background-color: rgb(2, 52, 10);
}

.details:hover{
  background-color: rgb(38, 91, 38);
}

.end-streak {
  font-size: small;
  background-color: rgb(164, 51, 62);
}

.end-streak:hover {
  background-color: rgb(199, 61, 75);
}

.show-matches {
  background-color: darkblue;
  border: 2px solid black;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  font-size: small;
}

.show-matches:hover {
  background-color: mediumblue;
}

table {
  height: 100%;
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  text-align: center;
  border-color: white;
}


</style>
