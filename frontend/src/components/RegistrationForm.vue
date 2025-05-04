<template>
  <div>
    <h2>Registration Form</h2>
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
        <label>Job Title:</label>
        <select v-model="jobTitle" required>
          <option disabled value="">Select job title</option>
          <option v-for="title in jobTitles" :key="title">{{ title }}</option>
        </select>
      </div>
      <div>
        <label>Job Area:</label>
        <select v-model="jobArea" required>
          <option disabled value="">Select job area</option>
          <option v-for="area in jobAreas" :key="area">{{ area }}</option>
        </select>
      </div>
      <div>
        <label>Education Level:</label>
        <select v-model="educationLevel" required>
          <option disabled value="">Select education level</option>
          <option v-for="level in educationLevels" :key="level">{{ level }}</option>
        </select>
      </div>
      <div>
        <label>Education Fields:</label>
        <div class="checkbox-list">
          <label v-for="field in educationFieldsList" :key="field" class="checkbox-label">
            <input type="checkbox" :value="field" v-model="educationFields" />
            {{ field }}
          </label>
        </div>
      </div>
      <div>
        <label>Universities:</label>
        <div class="checkbox-list">
          <label v-for="uni in universitiesList" :key="uni" class="checkbox-label">
            <input type="checkbox" :value="uni" v-model="universities" />
            {{ uni }}
          </label>
        </div>
      </div>
      <div>
        <label>Education Countries:</label>
        <div class="checkbox-list">
          <label v-for="country in educationCountriesList" :key="country" class="checkbox-label">
            <input type="checkbox" :value="country" v-model="educationCountries" />
            {{ country }}
          </label>
        </div>
      </div>
      <div>
        <label>Languages:</label>
        <div v-for="(lang, i) in languages" :key="i" class="language-row">
          <select v-model="lang.language">
            <option v-for="l in languagesList" :key="l">{{ l }}</option>
          </select>
          <select v-model="lang.level">
            <option v-for="lvl in languageLevels" :key="lvl">{{ lvl }}</option>
          </select>
          <button type="button" @click="removeLanguage(i)">Remove</button>
        </div>
        <button type="button" @click="addLanguage">Add Language</button>
      </div>
      <div>
        <label>Interests:</label>
        <div class="checkbox-list">
          <label v-for="interest in interestsList" :key="interest" class="checkbox-label">
            <input type="checkbox" :value="interest" v-model="interests" />
            {{ interest }}
          </label>
        </div>
      </div>
      <div>
        <label>Personality Type:</label>
        <select v-model="personalityType">
          <option v-for="type in personalityTypes" :key="type">{{ type }}</option>
        </select>
      </div>
      <div>
        <label>Career Goal:</label>
        <input v-model="careerGoal" />
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: "",
      lastName: "",
      jobTitle: "",
      jobArea: "",
      educationLevel: "",
      educationFields: [],
      universities: [],
      educationCountries: [],
      languages: [],
      interests: [],
      personalityType: "",
      careerGoal: "",
      jobTitles: [],
      jobAreas: [],
      educationLevels: [],
      educationFieldsList: [],
      universitiesList: [],
      educationCountriesList: [],
      languagesList: [],
      languageLevels: [],
      interestsList: [],
      personalityTypes: []
    };
  },
  methods: {
    addLanguage() {
      this.languages.push({ language: "", level: "" });
    },
    removeLanguage(i) {
      this.languages.splice(i, 1);
    },
    async submitForm() {
      const formData = {
        firstName: this.firstName,
        lastName: this.lastName,
        jobTitle: this.jobTitle,
        jobArea: this.jobArea,
        educationLevel: this.educationLevel,
        educationFields: this.educationFields,
        universities: this.universities,
        educationCountries: this.educationCountries,
        languages: this.languages,
        interests: this.interests,
        personalityType: this.personalityType,
        careerGoal: this.careerGoal
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
      this.jobTitle = "";
      this.jobArea = "";
      this.educationLevel = "";
      this.educationFields = [];
      this.universities = [];
      this.educationCountries = [];
      this.languages = [];
      this.interests = [];
      this.personalityType = "";
      this.careerGoal = "";
    },
    async fetchParameters() {
      const fetchParam = async (name, stateKey) => {
        const res = await fetch(`http://localhost:3001/api/parameters/${name}`);
        this[stateKey] = await res.json();
      };
      await Promise.all([
        fetchParam("job_titles", "jobTitles"),
        fetchParam("job_areas", "jobAreas"),
        fetchParam("education_levels", "educationLevels"),
        fetchParam("education_fields", "educationFieldsList"),
        fetchParam("universities", "universitiesList"),
        fetchParam("education_countries", "educationCountriesList"),
        fetchParam("languages", "languagesList"),
        fetchParam("language_levels", "languageLevels"),
        fetchParam("interests", "interestsList"),
        fetchParam("personality_types", "personalityTypes")
      ]);
    }
  },
  mounted() {
    this.fetchParameters();
  }
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  max-width: 420px;
  margin: 1.5rem auto;
  background: #f8f9fa;
  padding: 1.2rem 1.2rem;
  border-radius: 0.7rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

form label {
  font-weight: 500;
  margin-bottom: 0.1rem;
  display: block;
  font-size: 1rem;
}

.checkbox-list {
  display: block;
  margin-top: 0.2rem;
  padding: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-weight: normal;
  font-size: 1rem;
  margin-bottom: 0.1rem;
  gap: 0.2rem;
  cursor: pointer;
}

form button[type="submit"] {
  background: #0b3866;
  color: #fff;
  border: none;
  font-size: 1.1rem;
  margin-top: 0.7rem;
  cursor: pointer;
  border-radius: 0.3rem;
  padding: 0.6rem 0;
  transition: background 0.2s;
}

form button[type="submit"]:hover {
  background: #145ea8;
}

form > div {
  margin-bottom: 0.1rem;
}

.language-row {
  display: flex;
  gap: 0.3rem;
  align-items: center;
  margin-bottom: 0.2rem;
}

.language-row select {
  flex: 1 1 0;
  min-width: 0;
}

.language-row button {
  flex: 0 0 auto;
  padding: 0.2rem 0.5rem;
  font-size: 0.93rem;
  background: #eee;
  border: 1px solid #bbb;
  color: #333;
  border-radius: 0.2rem;
}

.language-row button:hover {
  background: #e0e0e0;
}

@media (max-width: 600px) {
  form {
    padding: 0.7rem 0.3rem;
    max-width: 98vw;
  }
  .checkbox-list {
    gap: 0.3rem 0.7rem;
  }
}
</style>
