<template>
    <div class="web-container">
      <h1>REGISTER!</h1>
      <MatchMeForm />
    </div>  
</template>

<script>
import MatchMeForm from "../components/MatchMeForm.vue";

export default {
  name: "MatchmakerView",
  components: {
    MatchMeForm,
  },
  data() {
    return {
        }
    }
}
</script>

<style scoped>
.web-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0b3866 0%, #2e8fff 100%);
  font-family: 'Inter', Arial, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}
header { margin-top: 3rem; text-align: center; }
h1 {
  font-size: 3rem;
  font-weight: 800;
  font-style: italic;
  color: #fff;
  letter-spacing: 2px;
  margin-bottom: 0.5rem;
  text-shadow: 0 4px 24px rgba(44,62,80,0.2);
}
.header-line {
  width: 80px; height: 6px;
  background: linear-gradient(90deg, #2e8fff 0%, #0b3866 100%);
  border-radius: 3px;
  margin: 0 auto 2rem;
}
</style>