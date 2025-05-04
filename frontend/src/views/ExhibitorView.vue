<template>
    <div>
      <h1>Registrera Utställare</h1>
      <ExhibitorForm />
    </div>

    <div>
      <h1>Alla utställare</h1>
      <button @click="fetchExhibitors">Hämta utställare</button>
      <div v-if="loading">Laddar utställare...</div>
      <div v-if="error" style="color: red;">{{ error }}</div>
      <div v-if="exhibitors.length">
        <div v-for="(exhibitor, index) in exhibitors" :key="index" style="margin-bottom: 20px;">
          <p>
            <span v-for="(value, key) in exhibitor" :key="key">
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
          </p>
        </div>
      </div>
    </div>
</template>

<script>
import ExhibitorForm from "../components/ExhibitorForm.vue";

export default {
  name: "ExhibitorView",
  components: {
    ExhibitorForm,
  },
  data() {
    return {
      matches: [],
      exhibitors: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchExhibitors() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch("http://localhost:3001/api/exhibitors");
        if (!response.ok) throw new Error("Kunde inte hämta utställare");
        this.exhibitors = await response.json();
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>