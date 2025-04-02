<template>
  <table>
    <thead>
      <tr>
        <th scope="col">Country</th>
        <th scope="col">Total</th>
        <th scope="col">Record (W-D-L)</th>
        <th scope="col">Date Started</th>
        <th scope="col">{{ showEnd ? 'Date Ended' : 'Details' }}</th>
      </tr>
    </thead>
    <tbody>
      <template class="temp" v-for="(streak, i) in streaks">
        <tr class="streak">
          <td>{{ streak.country }}</td>
          <td>{{ streak.total }}</td>
          <td>{{ streak.wins }}-{{ streak.draws }}-{{ streak.losses }}</td>
          <td>{{ streak.date_started }}</td>
          <td>
            {{ streak.details_end.date }}
            <button @click="showDetails[i] = !showDetails[i]" class="show-matches">
              {{ showDetails[i] ? 'Hide matches' : 'Show Matches' }}
            </button>
          </td>
        </tr>
        <tr class="details-header" v-show="showDetails[i]">
          <td>Date match</td>
          <td>Home team</td>
          <td>Result</td>
          <td>Away Team</td>
          <td>Tournament</td>
        </tr>
        <tr class="details" v-show="showDetails[i]" v-for="(detail, j) in streak.details_streak">
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
        </tr>

        <tr
          class="end-streak"
          v-if="showEnd"
          v-show="showDetails[i]"
          title="Match that ended the streak"
        >
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
.filler {
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;
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
  border: 1px none #dededf;
  color: white;
  height: 100%;
  width: 100%;
  table-layout: fixed;

  border-collapse: collapse;
  border-spacing: 5px;
  text-align: center;
}

caption {
  caption-side: top;
  text-align: left;
}

th {
  border: 1px none #dededf;
  background-color: rgb(55, 55, 65);
  padding: 5px;
}

td {
  border-bottom: 3px solid rgb(25, 25, 35);
  padding: 5px;
}

.streak {
  background-color: rgb(45, 45, 55);
}

.details {
  font-size: smaller;
  background-color: rgb(2, 52, 10);
}

.details-header {
  font-size: smaller;
  background-color: rgb(52, 52, 57);
}

.end-streak {
  font-size: smaller;
  background-color: rgb(199, 61, 75);
}
</style>
