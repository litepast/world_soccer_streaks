<template>
  <div class="main-container">
    <h1>WORLD FOOTBALL STREAKS</h1>
    <div class="last-update">Last update: {{ lastUpdate }}</div>
    <div class="description">
      Discover the national teams that have dominated and struggled the international stage! We're
      tracking the best and worst, all time and ongoing streaks in international Football! The top
      20 streaks of all time and top 5 ongoing streaks of each category will be shown, however there
      might be more if many streaks share their totals.<br /><br />
      The matches data is provided by
      <a
        href="https://www.kaggle.com/datasets/patateriedata/all-international-football-results"
        target="_blank"
      >
        This Kaggle Dataset</a
      >
    </div>
    <h2>Top Streaks of All-Time</h2>
    <div class="description">
      The top finished streaks that have left their mark in history.
    </div>
    <div class="inst">
      Click on a streak to show its match details and click on the details to hide them again. Streak ended on match on red.
    </div>
     

    <div class="button-type-container">
      <div @click="showAllTimeStreak(0)" style="padding-left: 10px;" :style="showAllTime[0] ? styleButtonSelected : null" class="selector">
        Unbeaten
      </div>
      <div @click="showAllTimeStreak(1)" :style="showAllTime[1] ? styleButtonSelected : null" class="selector">        
        Winning 
      </div>
      <div @click="showAllTimeStreak(2)" :style="showAllTime[2] ? styleButtonSelected : null" class="selector">        
        Losing
      </div>
      <div @click="showAllTimeStreak(3)" :style="showAllTime[3] ? styleButtonSelected : null" class="selector">        
        Winless
      </div>
      <div @click="showAllTimeStreak(4)" style="padding-right: 10px; ":style="showAllTime[4] ? styleButtonSelected : null" class="selector">        
        Drawing
      </div>
    </div>
    <div v-for="(streakType, i) in streakTypes" style="width: 100%">
      <div v-show="showAllTime[i]" class="table-container">
        <StreakTable :streaks="streaks.all_time[streakType]" :showEnd="true" />
      </div>
    </div>

    <h2>Top Active Streaks</h2>
    <div class="description">
      Streaks that are still running! Some teams might hope to extend them and some to end them!. Click on streak for match details
    </div>
    <div class="inst">
      Click on a streak to show its match details and click on the details to hide them again.
    </div>
    

    <div class="button-type-container">
      <div @click="showActiveStreak(0)" style="padding-left: 10px;" :style="showActive[0] ? styleButtonSelected : null" class="selector">
        Unbeaten
      </div>
      <div @click="showActiveStreak(1)" :style="showActive[1] ? styleButtonSelected : null" class="selector">        
        Winning 
      </div>
      <div @click="showActiveStreak(2)" :style="showActive[2] ? styleButtonSelected : null" class="selector">        
        Losing
      </div>
      <div @click="showActiveStreak(3)" :style="showActive[3] ? styleButtonSelected : null" class="selector">        
        Winless
      </div>
      <div @click="showActiveStreak(4)" style="padding-right: 10px; ":style="showActive[4] ? styleButtonSelected : null" class="selector">        
        Drawing
      </div>
    </div>



    <div v-for="(streakType, i) in streakTypes" style="width: 100%">
      <div v-show="showActive[i]" class="table-container">
        <StreakTable :streaks="streaks.active[streakType]" :showEnd="false" />
      </div>
    </div>
    <footer>
      Website created by Enrique Martínez<br />
      Kaggle dataset created by Clement Bravo<br />
      Website icon from
      <a href="https://icon-icons.com/icon/soccer-football/34114" target="_blank">icon-icons.com</a>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StreakTable from './components/StreakTable.vue'
import streaks from './data/streaks.json'
const streakTypes = ['Unbeaten', 'Winning', 'Losing', 'Winless', 'Drawing']
const lastUpdate = new Date(streaks.date_updated).toLocaleString('es-MX', { timeZoneName: 'short' })
const styleButtonSelected = 'font-weight: bold; color: white; border-bottom: 2px solid white;'
const showAllTime = ref(Array(5).fill(false))
const showActive = ref(Array(5).fill(false))

showAllTime.value[0] = true
showActive.value[0] = true



function showAllTimeStreak(a) {
  showAllTime.value.fill(false)
  showAllTime.value[a] = true
}

function showActiveStreak(a) {
  showActive.value.fill(false)
  showActive.value[a] = true
}
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: auto;
  width: 100%;
}

h1 {
  width: 100%;
  height: auto;
  text-align: center;
  padding: 5px;
  font-size: 2.5em;
  font-family: Impact;
}

h2 {
  width: 100%;
  text-align: left;
  padding: 10px;
}
.last-update {
  width: 100%;
  text-align: right;
  padding: 10px;
  font-size: xx-small;
}

.description {
  width: 100%;
  justify-content: left;
  text-align: left;
  padding-left: 10px;
  padding-right: 10px;
}

.inst{
  width: 100%;
  font-size: small;
  justify-content: left;
  padding-left: 10px;
  padding-right: 10px;
  padding-bottom: 10px;
}

.button-type-container {
  display: grid;  
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  text-align: center;
  width: 100%;
  padding-top: 15px;
  color: rgb(160, 161, 175);
  background-color: rgb(16, 18, 24);
  border: 1px solid rgb(54, 58, 66);
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
}

.selector{
  height: 100%;
  padding-bottom: 15px;
  cursor: pointer;
}


a:link {
  color: white;
  background-color: transparent;
  text-decoration: underline;
}
a:visited {
  color: darkcyan;
  background-color: transparent;
  text-decoration: underline;
}
a:hover {
  color: blueviolet;
  background-color: transparent;
  text-decoration: underline;
}
a:active {
  color: darkmagenta;
  background-color: transparent;
  text-decoration: underline;
}

.table-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  border-left: 1px solid rgb(54, 58, 66);
  border-right: 1px solid  rgb(54, 58, 66);
  border-bottom: 1px solid  rgb(54, 58, 66);
}

footer {
  font-size: medium;
  text-align: center;
  padding: 10px;
  margin: 10px;
}
</style>
