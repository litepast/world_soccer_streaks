<template>
  <table>
    <thead>
      <tr class="top-header">
        <td class="side-col"></td>
        <td>Country</td>
        <td>Total</td>
        <td>Record (W-D-L)</td>
        <td>Date Started</td>
        <td>{{ showEnd ? 'Date Ended' : 'Details' }}</td>
        <td class="side-col"></td>
      </tr>
    </thead>
    <tbody>
      <template class="temp" v-for="(streak, i) in streaks">
        <tr class="streak">
          <td class="side-col"></td>
          <td>{{ streak.country }}</td>
          <td>{{ streak.total }}</td>
          <td>{{ streak.wins }}-{{ streak.draws }}-{{ streak.losses }}</td>
          <td>{{ streak.date_started }}</td>
          <td>
            {{ streak.details_end.date }}
            <button @click="showDetails[i] = !showDetails[i]" class="show-matches">
              {{ showDetails[i] ? 'Hide matches' : '⌄' }}
            </button>
          </td>
          <td class="side-col"></td>
        </tr>
        <tr class="details-header" v-show="showDetails[i]">
          <td class="side-col"></td>
          <td>Date match</td>
          <td>Home team</td>
          <td>Result</td>
          <td>Away Team</td>
          <td>Tournament</td>
          <td class="side-col"></td>
        </tr>
        <tr class="details" v-show="showDetails[i]" v-for="(detail, j) in streak.details_streak">
          <td class="side-col"></td>
          <td>{{ detail.date }}</td>
          <td :style="countryBold(streak.country, detail.home_team)">{{ detail.home_team }}</td>
          <td>{{ detail.home_score }} - {{ detail.away_score }}</td>
          <td :style="countryBold(streak.country, detail.away_team)">{{ detail.away_team }}</td>
          <td style="overflow-wrap: break-word">
            {{ detail.tournament }}
            <button
              v-if="j == streak.details_streak.length - 1 && !showEnd"
              @click="showDetails[i] = !showDetails[i]"
              class="show-matches"
            >
              Hide matches
            </button>
          </td>
          <td class="side-col"></td>
        </tr>

        <tr
          class="end-streak"
          v-if="showEnd"
          v-show="showDetails[i]"
          title="Match that ended the streak"
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
          <td>
            {{ streak.details_end.tournament }}
            <button @click="showDetails[i] = !showDetails[i]" class="show-matches">
              Hide matches
            </button>
          </td>
          <td class="side-col"></td>
        </tr>
      </template>
      <!-- <tr v-show="showFiller" class="filler" v-for="n in diff" style="color: white">
        <td colspan="1">{{ '\u00A0' }}</td>
      </tr> -->
    </tbody>
  </table>
</template>

<script setup>
import { ref, defineProps, computed } from 'vue'
const showDetails = ref(Array(streaks.length).fill(false))

// const showFiller = computed(() => {
//   return showDetails.value.every((val) => val === false)
// })

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

.end-streak {
  font-size: small;
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
}




/* .filler {
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;
} */

</style>
