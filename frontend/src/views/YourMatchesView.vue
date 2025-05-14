<template>
  <div class="people-view">
    <h1>MATCHMAKING</h1>
    <div v-if="loading" class="loading">Laddar matcher...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="match && match.all_matches && displayedMatches.length" class="person-card">
      <div class="person-header">
        <span class="person-name">{{ match.person.firstName }} {{ match.person.lastName }}</span>
        <span class="person-job">{{ match.person.jobTitle }} ({{ match.person.jobArea }})</span>
        <div class="person-divider"></div>
        <span class="person-interests">
          <span
            v-for="(interest, i) in match.person.interests"
            :key="i"
            class="interest-chip"
          >
            {{ interest }}
          </span>
        </span>
        <span class="person-goal">
          Primary event goal: {{ match.person.eventGoals[0] }}
        </span>
      </div>
      <div class="matches-section">
        <h3>Your Top 3 Matches:</h3>
        <div class="matches-list">
          <div
            v-for="(top, i) in displayedMatches"
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
                    <text
                      x="20"
                      y="24"
                      text-anchor="middle"
                      font-size="13"
                      fill="#0b3866"
                      font-weight="bold"
                    >
                      {{ getPercentage(top.score) }}%
                    </text>
                  </g>
                </svg>
              </div>
            </div>
            <div class="match-header">
              <span
                class="match-company"
                v-if="top.exhibitor.company"
              >
                {{ top.exhibitor.company }}
              </span>
              <div class="match-divider"></div>
              <span class="match-name">
                {{ top.exhibitor.firstName }} {{ top.exhibitor.lastName }}
              </span>
              <span class="match-job">
                {{ top.exhibitor.jobTitle }}
              </span>
              <span class="match-interests">
                <span
                  v-for="(interest, j) in top.exhibitor.interests"
                  :key="j"
                  class="interest-chip"
                >
                  {{ interest }}
                </span>
              </span>
              <span class="match-goal">
                Primary event goal: {{ top.exhibitor.eventGoals[0] }}
              </span>
            </div>
            <button class="refresh-btn" @click="refreshMatch(i)">Swap</button>
            <template v-if="i === 0 && sameFirstChoicePeople.length">
              <div class="others-matched-section">
                <div class="others-matched-title">Others who matched:</div>
                <div class="others-matched-list">
                  <div
                    v-for="(person, idx) in sameFirstChoicePeople"
                    :key="idx"
                    class="profile-initials"
                    :title="person.person.firstName + ' ' + person.person.lastName"
                  >
                    {{ getInitials(person.person.firstName, person.person.lastName) }}
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="!loading && !error">
      <div class="error">
        Ingen persondata hittades. Gå tillbaka och fyll i formuläret.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "YourMatchesView",
  data() {
    return {
      match: null,
      loading: false,
      error: null,
      bestMatchColor: "#1976d2",
      circumference: 2 * Math.PI * 18,
      allMatches: [],
      displayedIndexes: [0, 1, 2], // index i all_matches som visas på plats 1, 2, 3
    };
  },
  computed: {
    displayedMatches() {
      if (!this.match || !this.match.all_matches) return [];
      return this.displayedIndexes.map(idx => this.match.all_matches[idx]);
    },
    sameFirstChoicePeople() {
      if (!this.match || !this.allMatches.length) return [];
      const myFirst = this.match.all_matches[this.displayedIndexes[0]];
      if (!myFirst) return [];
      return this.allMatches.filter(
        m =>
          m.all_matches &&
          m.all_matches.length &&
          m.all_matches[0].exhibitor.firstName === myFirst.exhibitor.firstName &&
          m.all_matches[0].exhibitor.lastName === myFirst.exhibitor.lastName &&
          (m.person.firstName !== this.match.person.firstName ||
            m.person.lastName !== this.match.person.lastName)
      );
    },
  },
  methods: {
    refreshMatch(pos) {
      if (!this.match || !this.match.all_matches) return;
      const used = new Set(this.displayedIndexes);
      let nextIdx = this.displayedIndexes[pos] + 1;
      while (nextIdx < this.match.all_matches.length && used.has(nextIdx)) {
        nextIdx++;
      }
      if (nextIdx < this.match.all_matches.length) {
        // Gör en kopia och byt ut indexet, så Vue ser ändringen
        const newIndexes = [...this.displayedIndexes];
        newIndexes[pos] = nextIdx;
        this.displayedIndexes = newIndexes;
      }
    },
    getPercentage(score) {
      return Math.round(Math.max(0, Math.min(100, score)));
    },
    async fetchMatch() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch("http://localhost:3001/api/me/matches");
        if (!response.ok) throw new Error();
        this.match = await response.json();
        this.displayedIndexes = [0, 1, 2];
      } catch {
        this.error = "Kunde inte hämta matchningsresultat.";
      } finally {
        this.loading = false;
      }
    },
    async fetchAllMatches() {
      try {
        const response = await fetch("http://localhost:3001/api/matches");
        if (!response.ok) throw new Error();
        this.allMatches = await response.json();
      } catch {
        this.allMatches = [];
      }
    },
    async cleanupMeFile() {
      await fetch("http://localhost:3001/api/me", { method: "DELETE" });
    },
    getInitials(first, last) {
      return (first?.[0] || "") + (last?.[0] || "");
    },
  },
  mounted() {
    this.fetchMatch();
    this.fetchAllMatches();
  },
  beforeUnmount() {
    this.cleanupMeFile();
  },
};
</script>

<style scoped>
:global(body) {
  min-height: 110vh;
  background: linear-gradient(135deg, #0b3866 0%, #2e8fff 100%);
}
.people-view {
  max-width: 900px;
  margin: 0 auto;
  margin-top: 1.5rem;
  padding: 2rem 1rem;
  background: #f8f9fa;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.people-view h1 {
  font-size: 4rem;
  color: #0b3866;
  margin-top: 0.3rem;
  margin-bottom: 1.5rem;
  font-style: italic;
}
.loading,
.error {
  margin: 1rem 0;
  font-size: 1.2rem;
  text-align: center;
}
.person-card {
  background: #fff;
  border-radius: 0.7rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  padding: 1.5rem 1rem 1rem 1rem;
  margin-top: 2rem;
  min-width: 220px;
  min-height: 180px;
  border: 2px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
  overflow: visible;
}
.person-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-weight: 600;
  color: #0b3866;
  margin-bottom: 0.2rem;
  margin-top: 0.5rem;
  width: 100%;
}
.person-name {
  font-size: 2.5rem;
  font-weight: 600;
  color: #0b3866;
}
.person-job {
  display: block;
  font-size: 1rem;
  font-style: italic;
  color: #424242;
  margin-top: 0.2rem;
  margin-bottom: 0.2rem;
}
.person-divider {
  width: 100%;
  border-bottom: 2px solid #e0e0e0;
  margin-bottom: 0.7rem;
}
.person-interests {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-bottom: 0.2rem;
  justify-content: flex-start;
  width: 100%;
}
.person-goal {
  font-size: 0.95rem;
  font-weight: 500;
  font-style: italic;
  color: #555;
  margin-top: 0.7rem;
}
.matches-section {
  margin-top: 2rem;
}
.matches-section h3 {
  font-size: 1.2rem;
  margin-bottom: 2rem;
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
  min-width: 220px;
  height: 340px;         /* Fixerad höjd */
  min-height: 340px;     /* Säkerställ minsta höjd */
  border: 2px solid #e0e0e0;
  transition: border 0.2s;
  overflow: visible;
  position: relative;
  padding-bottom: 3.2rem; /* ge plats för knappen */
  margin-bottom: 2.5rem;
}
.match-card.best-match {
  border: 2.5px solid #1976d2;
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
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-weight: 600;
  color: #0b3866;
  margin-bottom: 0.2rem;
  margin-top: 0.5rem;
}
.match-name {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1976d2;
}
.match-company {
  color: #0b3866;
  font-size: 1.6rem;
  margin-top: -1rem;
  margin-bottom: 0.5rem;
}
.match-divider {
  width: 230px;
  border-bottom: 2px solid #e0e0e0;
  margin-bottom: 0.5rem;
}
.match-job {
  display: block;
  font-size: 1rem;
  font-style: italic;
  color: #424242;
  margin-top: 0.2rem;
  margin-bottom: 0.8rem;
}
.match-interests {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  margin-bottom: 0.2rem;
}
.match-goal {
  margin-top: 2rem;
  font-size: 0.95rem;
  font-weight: 500;
  font-style: italic;
  color: #555;
}
.interest-chip {
  background: #d7e6f5;
  color: #337bc4;
  border-radius: 0.7em;
  padding: 0.13em 0.7em;
  font-size: 0.93em;
  margin: 0 0 0.1em 0;
  display: block;
  align-self: flex-start;
  box-sizing: border-box;
  font-family: inherit;
  font-weight: 500;
}
.refresh-btn {
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translate(-50%, 50%);
  background: #e3f0fd;
  color: #1976d2;
  border: 1.5px solid #b6d4fa;
  border-radius: 0.5rem;
  padding: 0.4rem 1.2rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  z-index: 2;
  box-shadow: 0 2px 8px rgba(44,62,80,0.10);
}
.refresh-btn:hover {
  background: #1976d2;
  color: #fff;
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
.others-matched-section {
  margin-top: 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}
.others-matched-title {
  font-size: 1rem;
  font-weight: 600;
  color: #0b3866;
  margin-bottom: 0.3rem;
}
.others-matched-list {
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
}
.profile-initials {
  width: 2.4rem;
  height: 2.4rem;
  border-radius: 50%;
  background: #e3f0fd;
  color: #1976d2;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 1px 4px rgba(25,118,210,0.08);
  cursor: pointer;
  transition: background 0.2s;
  border: 2px solid #b6d4fa;
}
.profile-initials:hover {
  background: #1976d2;
  color: #fff;
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