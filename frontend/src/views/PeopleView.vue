<template>
    <div>
      <h1>Registrera Person</h1>
      <RegistrationForm />
    </div>
    
    <div>
      <h1>Matchade personer</h1>
      <button @click="fetchMatches">Hämta matcher</button>
      <div v-if="loading">Laddar matcher...</div>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <div v-if="matches.length">
        <div
          v-for="(match, index) in matches"
          :key="index"
          style="margin-bottom: 20px;"
        >
          <p>
            <strong>{{ match.person.firstName }} {{ match.person.lastName }}</strong><br>
            <span v-for="(value, key) in match.person" :key="key" v-if="key !== 'firstName' && key !== 'lastName'">
              <span style="font-weight:600;">{{ key }}:</span>
              <span v-if="Array.isArray(value)">
                <span v-for="(item, idx) in value" :key="idx">
                  <span v-if="typeof item === 'object'">{{ item.language }} ({{ item.level }})<span v-if="idx < value.length-1">, </span></span>
                  <span v-else>{{ item }}<span v-if="idx < value.length-1">, </span></span>
                </span>
              </span>
              <span v-else>{{ value }}</span>
              <br>
            </span>
            <br>
            <span style="font-weight:600;">Top Matches:</span><br>
            <span v-for="(top, i) in match.top_matches" :key="i">
              {{ i+1 }}.
              <span v-for="(value, key) in top.exhibitor" :key="key">
                <span v-if="key === 'firstName' || key === 'lastName'">{{ value }} </span>
              </span>
              ({{ top.exhibitor.company }}) – {{ top.exhibitor.jobArea }} ({{ top.exhibitor.jobTitle }})
              <span v-if="top.score !== undefined">[Poäng: {{ top.score }}]</span>
              <br>
              <span v-for="(value, key) in top.exhibitor" :key="key" v-if="!['firstName','lastName','company','jobArea','jobTitle'].includes(key)">
                <span style="font-weight:600;">{{ key }}:</span>
                <span v-if="Array.isArray(value)">
                  <span v-for="(item, idx) in value" :key="idx">
                    <span v-if="typeof item === 'object'">{{ item.language }} ({{ item.level }})<span v-if="idx < value.length-1">, </span></span>
                    <span v-else>{{ item }}<span v-if="idx < value.length-1">, </span></span>
                  </span>
                </span>
                <span v-else>{{ value }}</span>
                <br>
              </span>
              <br>
            </span>
          </p>
        </div>
      </div>
    </div>
</template>

<script>
import RegistrationForm from "../components/RegistrationForm.vue";
import axios from "axios";

export default {
  name: "PeopleView",
  components: {
    RegistrationForm,
  },
  data() {
    return {
      matches: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchMatches() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("http://localhost:3001/api/matches");
        this.matches = response.data;
      } catch (error) {
        this.error = "Kunde inte hämta matcher";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>