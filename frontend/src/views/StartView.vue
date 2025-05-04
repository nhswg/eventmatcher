<template>
  <div class="sketchdle-container">
    <header>
      <h1>Event Matchmaking</h1>
    </header>
    <div class="header-line"></div>

    <main>
      <div>
        <div class="buttons">
          <router-link to="/people/">
            <button class="button">
              People
            </button>
          </router-link>

          <router-link to="/exhibitors/">
            <button class="button">
              Exhibitors
            </button>
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'StartView',
  data() {
    return {
    }
  },
  created() {
  },
}
</script>

<style scoped>
.buttons {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-top: 10rem;
    color: #0b3866
}

.button {
    font-size: 3.5rem;
    width: 350px;
    height: 200px;
    border: 5px solid #0b3866;
    color: #0b3866;
    border-radius: 1rem;
}

@media (max-width: 600px) {
  .game-buttons {
    gap: 1rem;
  }
}
</style>