<template>
  <div class="people-view">
    <h1>Dina toppmatchade utställare</h1>
    <div v-if="loading" class="loading">Laddar matcher...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="match && match.top_matches.length" class="person-card">
      <div class="person-header">
        <span class="person-name">{{ match.person.firstName }} {{ match.person.lastName }}</span>
        <span class="person-job">{{ match.person.jobTitle }} – {{ match.person.jobArea }}</span>
        <span class="person-interests">
          <span v-for="(interest, i) in match.person.interests" :key="i" class="interest-chip">{{ interest }}</span>
        </span>
        <span class="person-goal">Mål: {{ match.person.eventGoals[0] }}</span>
      </div>
      <div class="matches-section">
        <h3>Topp 3 utställare</h3>
        <div class="matches-list">
          <div
            v-for="(top, i) in match.top_matches"
            :key="i"
            class="match-card"
            :class="{ 'best-match': i === 0 }"
          >
            <div class="match-score-container">
              <div class="circle-container">
                <svg viewBox="0 0 40 40" class="score-circle">
                  <circle
                    class="circle-bg"
                    cx="20"
                    cy="20"
                    r="18"
                    fill="none"
                    stroke="#e0e0e0"
                    stroke-width="4"
                  />
                  <circle
                    class="circle-fg"
                    cx="20"
                    cy="20"
                    r="18"
                    fill="none"
                    :stroke="bestMatchColor"
                    stroke-width="4"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="circumference - (getPercentage(top.score) / 100) * circumference"
                    stroke-linecap="round"
                  />
                  <g>
                    <text x="20" y="24" text-anchor="middle" font-size="13" fill="#0b3866" font-weight="bold">
                      {{ getPercentage(top.score) }}%
                    </text>
                  </g>
                </svg>
              </div>
            </div>
            <div class="match-header">
              <span class="match-name">
                {{ top.exhibitor.firstName }} {{ top.exhibitor.lastName }}
              </span>
              <span class="match-company" v-if="top.exhibitor.company">({{ top.exhibitor.company }})</span>
            </div>
            <div class="match-details">
              <span class="match-job">{{ top.exhibitor.jobTitle }} – {{ top.exhibitor.jobArea }}</span>
              <span class="match-interests">
                <span v-for="(interest, j) in top.exhibitor.interests" :key="j" class="interest-chip">{{ interest }}</span>
              </span>
              <span class="match-goal">Mål: {{ top.exhibitor.eventGoals[0] }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="!loading && !error">
      <div class="error">Ingen persondata hittades. Gå tillbaka och fyll i formuläret.</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "YourMatchesView",
  data() {
    return {
      match: null,
      loading: false,
      error: null,
      bestMatchColor: "#1976d2",
      circumference: 2 * Math.PI * 18,
    };
  },
  methods: {
    getPercentage(score) {
      let percent = Math.round(Math.max(0, Math.min(100, score)));
      return percent;
    },
    async fetchMatch() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch("http://localhost:3001/api/me/matches");
        if (!response.ok) throw new Error("Matchning misslyckades");
        this.match = await response.json();
      } catch (e) {
        this.error = "Kunde inte hämta matchningsresultat.";
      } finally {
        this.loading = false;
      }
    },
    async cleanupMeFile() {
      await fetch("http://localhost:3001/api/me", { method: "DELETE" });
    }
  },
  mounted() {
    this.fetchMatch();
  },
  beforeUnmount() {
    this.cleanupMeFile();
  },
};
</script>

<style scoped>
.people-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}
.loading, .error {
  margin: 1rem 0;
  font-size: 1.2rem;
  text-align: center;
}
.person-card {
  background: #f8f9fa;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 1.5rem 1.5rem 1.2rem 1.5rem;
  margin-top: 2rem;
}
.person-header {
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.7rem;
  margin-bottom: 1.2rem;
}
.person-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0b3866;
}
.person-job {
  display: block;
  font-size: 1.1rem;
  color: #1976d2;
  margin-top: 0.2rem;
  margin-bottom: 0.2rem;
}
.person-interests {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-bottom: 0.2rem;
}
.person-goal {
  font-size: 1rem;
  color: #555;
}
.matches-section {
  margin-top: 0.5rem;
}
.matches-section h3 {
  font-size: 1.1rem;
  margin-bottom: 0.7rem;
  color: #0b3866;
}
.matches-list {
  display: flex;
  flex-direction: row;
  gap: 1.2rem;
  flex-wrap: wrap;
}
.match-card {
  flex: 1 1 220px;
  background: #fff;
  border-radius: 0.7rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  padding: 1.5rem 1rem 1rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
  min-width: 220px;
  min-height: 180px;
  border: 2px solid #e0e0e0;
  transition: border 0.2s;
  overflow: visible;
}
.match-card.best-match {
  border: 2.5px solid #1976d2;
  background: #e3f0fd;
}
.match-score-container {
  position: absolute;
  top: -24px;
  right: -24px;
  z-index: 2;
  background: #e3f0fd;
  border-radius: 50%;
  box-shadow: 0 1px 4px rgba(25,118,210,0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border: 3px solid #fff;
}
.match-header {
  font-size: 1.1rem;
  font-weight: 600;
  color: #0b3866;
  margin-bottom: 0.2rem;
  margin-top: 0.5rem;
}
.match-company {
  color: #1976d2;
  font-size: 1rem;
  margin-left: 0.2rem;
}
.match-details {
  font-size: 0.98rem;
  color: #444;
  margin-bottom: 0.5rem;
}
.match-job {
  display: block;
  font-size: 1rem;
  color: #1976d2;
  margin-bottom: 0.2rem;
}
.match-interests {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem;
  margin-bottom: 0.2rem;
}
.match-goal {
  font-size: 0.95rem;
  color: #555;
}
.interest-chip {
  background: #e0e7ef;
  color: #1976d2;
  border-radius: 0.7em;
  padding: 0.13em 0.7em;
  font-size: 0.93em;
  margin-right: 0.1em;
  margin-bottom: 0.1em;
  display: inline-block;
}
.circle-container {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.score-circle {
  width: 44px;
  height: 44px;
}
.circle-bg,
.circle-fg {
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}
@media (max-width: 900px) {
  .matches-list {
    flex-direction: column;
    gap: 1rem;
  }
  .match-card {
    min-width: 0;
    width: 100%;
    padding-top: 1.5rem;
  }
  .match-score-container {
    top: -18px;
    right: -18px;
    width: 40px;
    height: 40px;
  }
}
</style>