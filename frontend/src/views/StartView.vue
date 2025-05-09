<template>
  <div class="web-container">
    <header>
      <h1>EVENTMATCHER</h1>
    </header>
    <div class="header-line"></div>
    <main>
      <div class="main-buttons">
        <router-link to="/matchmaker/"><button class="matchmake-btn">MATCHMAKE ME!</button></router-link>
        <div class="extra-buttons">
          <router-link to="/people/"><button class="extra-button">PEOPLE</button></router-link>
          <router-link to="/exhibitors/"><button class="extra-button">EXHBITORS</button></router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default { name: 'StartView' }
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
header {
  margin-top: 3rem;
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
  padding-left: 3rem;
  box-sizing: border-box;
}
h1 {
  font-family: 'Montserrat', 'Inter', Arial, sans-serif;
  font-size: 3rem;
  font-style: bold;
  color: rgba(255,255,255,0.92);
  letter-spacing: 2px;
  margin-top: 0rem;
  margin-bottom: 2rem;
  text-shadow: 0 4px 24px rgba(44,62,80,0.2);
}
.header-line {
  width: 95%; height: 10px;
  background: linear-gradient(90deg, #2e8fff 0%, #0b3866 100%);
  border-radius: 3px;
  margin: 0 auto 2rem;
}
.main-buttons {
  display: flex; flex-direction: column; align-items: center;
  margin-top: 10vh; gap: 3.5rem;
}
.matchmake-btn {
  font-size: 3rem; font-weight: 800; font-style: italic;
  width: 520px; height: 130px; margin-bottom: 2.5rem;
  background: linear-gradient(90deg, #00e6d0 0%, #2e8fff 100%);
  color: #0b3866; border: none; border-radius: 1rem;
  cursor: pointer; letter-spacing: 1.5px;
  transition: transform 0.18s, box-shadow 0.18s, background 0.18s, color 0.18s;
  display: flex; align-items: center; justify-content: center;
}
.matchmake-btn:hover {
  background: linear-gradient(90deg, #2e8fff 0%, #00e6d0 100%);
  color: #fff; transform: translateY(-6px) scale(1.04);
}
.main-buttons a {
  text-decoration: none;
}
.extra-buttons {
  display: flex; justify-content: center; gap: 2.5rem; width: 100%;
}
.extra-button {
  font-size: 1.5rem; font-weight: 600; font-style: italic;
  width: 240px; height: 80px; border: none;
  color: #0b3866; border-radius: 1.5rem;
  background: rgba(255,255,255,0.92);
  cursor: pointer;
  transition: background 0.18s, color 0.18s, transform 0.15s;
  display: flex; align-items: center; justify-content: center;
  letter-spacing: 0.5px; backdrop-filter: blur(2px);
}
.extra-button:hover {
  background: linear-gradient(90deg, #2e8fff 0%, #00e6d0 100%);
  color: #fff; transform: translateY(-3px) scale(1.03);
}
</style>