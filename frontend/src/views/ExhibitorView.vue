<template>
  <div class="web-container">
    <h1>REGISTER (EXHIBITOR)</h1>
    <ExhibitorForm />
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

<style scoped>
.web-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0b3866 0%, #2e8fff 100%);
  font-family: 'Inter', Arial, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 2rem;
}
h1 {
  font-size: 2.2rem;
  font-weight: 800;
  font-style: italic;
  color: #fff;
  letter-spacing: 2px;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 24px rgba(44,62,80,0.2);
  margin-top: 2rem;
}
.all-exhibitors-section {
  width: 100%;
  max-width: 900px;
  margin: 2rem auto 0 auto;
  background: #f8f9fa;
  border-radius: 1.2rem;
  box-shadow: 0 2px 12px rgba(44,62,80,0.07);
  padding: 2rem 2rem 1.5rem 2rem;
}
.fetch-btn {
  background: linear-gradient(90deg, #00e6d0 0%, #2e8fff 100%);
  color: #0b3866;
  border: none;
  font-size: 1.1rem;
  font-weight: 700;
  font-style: italic;
  margin-bottom: 1.2rem;
  cursor: pointer;
  border-radius: 0.7rem;
  padding: 0.7rem 2.2rem;
  transition: background 0.18s, color 0.18s, transform 0.15s, box-shadow 0.18s;
  box-shadow: 0 4px 18px 0 rgba(44,62,80,0.13), 0 1.5px 8px 0 #00e6d055;
  letter-spacing: 1.2px;
}
.fetch-btn:hover {
  background: linear-gradient(90deg, #2e8fff 0%, #00e6d0 100%);
  color: #fff;
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 8px 32px 0 rgba(44,62,80,0.18), 0 2px 12px 0 #2e8fff55;
}
.exhibitor-card {
  background: #fff;
  border-radius: 0.7rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  padding: 1.5rem 1rem 1rem 1rem;
  margin-bottom: 1.5rem;
  color: #0b3866;
  font-size: 1.05rem;
}
@media (max-width: 900px) {
  .all-exhibitors-section {
    padding: 1.2rem 0.5rem;
    max-width: 99vw;
  }
}
</style>