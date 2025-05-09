<template>
  <div>
    <form @submit.prevent="submitForm">
      <div>
        <label>First Name:</label>
        <input v-model="firstName" required />
      </div>
      <div>
        <label>Last Name:</label>
        <input v-model="lastName" required />
      </div>
      <div>
        <label>Job Area:</label>
        <select v-model="jobArea" required>
          <option disabled value="">Select job area</option>
          <option v-for="area in jobAreas" :key="area">{{ area }}</option>
        </select>
      </div>
      <div>
        <label>Job Title:</label>
        <select v-model="jobTitle" required>
          <option disabled value="">Select job title</option>
          <option v-for="title in jobTitles" :key="title">{{ title }}</option>
        </select>
      </div>
      <div>
        <label>Event Goal:</label>
        <select v-model="eventGoal" required>
          <option disabled value="">Select event goal</option>
          <option v-for="goal in eventGoalsList" :key="goal">{{ goal }}</option>
        </select>
      </div>
      <div>
        <label>Interests (max 3):</label>
        <div class="checkbox-list">
          <label v-for="interest in interestsList" :key="interest" class="checkbox-label">
            <input
              type="checkbox"
              :value="interest"
              v-model="interests"
              :disabled="interests.length >= 3 && !interests.includes(interest)"
            />
            {{ interest }}
          </label>
        </div>
      </div>
      <button type="submit">SUBMIT!</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: "",
      lastName: "",
      jobArea: "",
      jobTitle: "",
      interests: [],
      eventGoal: "",
      jobAreas: [],
      jobTitles: [],
      interestsList: [],
      eventGoalsList: [],
    };
  },
  methods: {
    async fetchParameters() {
      const fetchParam = async (name, stateKey) => {
        const res = await fetch(`http://localhost:3001/api/parameters/${name}`);
        this[stateKey] = await res.json();
      };
      await Promise.all([
        fetchParam("job_areas", "jobAreas"),
        fetchParam("job_titles", "jobTitlesRaw"),
        fetchParam("interests", "interestsList"),
        fetchParam("event_goals", "eventGoalsList"),
      ]);
      // Flatten jobTitlesRaw to a single array
      this.jobTitles = Object.values(this.jobTitlesRaw).flat();
    },
    async submitForm() {
      const formData = {
        firstName: this.firstName,
        lastName: this.lastName,
        jobArea: this.jobArea,
        jobTitle: this.jobTitle,
        interests: this.interests,
        eventGoals: [this.eventGoal],
      };
      await fetch("http://localhost:3001/api/people", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      this.resetForm();
    },
    resetForm() {
      this.firstName = "";
      this.lastName = "";
      this.jobArea = "";
      this.jobTitle = "";
      this.interests = [];
      this.eventGoal = "";
    },
  },
  mounted() {
    this.fetchParameters();
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  max-width: 600px;
  width: 98vw;
  margin: 2.5rem auto;
  background: linear-gradient(120deg, #e3f0fd 0%, #f8faff 100%);
  padding: 2.2rem 2.2rem 1.7rem 2.2rem;
  border-radius: 1.2rem;
  box-shadow: 0 8px 32px rgba(44,62,80,0.13), 0 1.5px 8px 0 #2e8fff22;
  border: 1.5px solid #b7d8ff;
}

form label {
  font-weight: 700;
  margin-bottom: 0.3rem;
  display: block;
  font-size: 1.08rem;
  color: #0b3866;
  letter-spacing: 0.5px;
}

input,
select {
  width: 100%;
  padding: 0.7rem 1rem;
  border: 1.5px solid #b7d8ff;
  border-radius: 0.6rem;
  font-size: 1.08rem;
  background: #fff;
  color: #0b3866;
  transition: border 0.18s, box-shadow 0.18s;
  box-shadow: 0 1px 4px rgba(44,62,80,0.07);
  outline: none;
}

input:focus,
select:focus {
  border-color: #2e8fff;
  box-shadow: 0 0 0 2px #2e8fff33;
}

.checkbox-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.2rem 0.5rem;
  margin-top: 0.1rem;
  padding: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  font-size: 0.95rem;
  gap: 0.2rem;
  cursor: pointer;
  color: #1976d2;
  background: #f3f8ff;
  border-radius: 0.4rem;
  padding: 0.08rem 0.4rem 0.08rem 0.2rem;
  transition: background 0.15s;
}

.checkbox-label input[type="checkbox"] {
  accent-color: #2e8fff;
  width: 1.1em;
  height: 1.1em;
}

.checkbox-label:hover {
  background: #e3f0fd;
}

form button[type="submit"] {
  background: linear-gradient(90deg, #00e6d0 0%, #2e8fff 100%);
  color: #0b3866;
  border: none;
  font-size: 1.2rem;
  font-weight: 800;
  font-style: italic;
  margin-top: 1.2rem;
  cursor: pointer;
  border-radius: 0.7rem;
  padding: 1rem 0;
  transition: background 0.18s, color 0.18s, transform 0.15s, box-shadow 0.18s;
  box-shadow: 0 4px 18px 0 rgba(44,62,80,0.13), 0 1.5px 8px 0 #00e6d055;
  letter-spacing: 1.2px;
}

form button[type="submit"]:hover {
  background: linear-gradient(90deg, #2e8fff 0%, #00e6d0 100%);
  color: #fff;
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 8px 32px 0 rgba(44,62,80,0.18), 0 2px 12px 0 #2e8fff55;
}

form > div {
  margin-bottom: 0.1rem;
}

@media (max-width: 700px) {
  form {
    padding: 1.2rem 0.5rem;
    max-width: 99vw;
  }
  .checkbox-list {
    gap: 0.3rem 0.5rem;
  }
}
</style>
