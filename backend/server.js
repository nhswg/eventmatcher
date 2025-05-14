const path = require('path');
const express = require('express');
const fs = require('fs');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

// Filhantering
function readJsonFile(filename) {
  if (fs.existsSync(filename)) {
    return JSON.parse(fs.readFileSync(filename));
  }
  return [];
}

function writeJsonFile(filename, data) {
  fs.writeFileSync(filename, JSON.stringify(data, null, 2));
}

// Validering för person
function isValidPerson(person) {
  return (
    person.firstName &&
    person.lastName &&
    person.jobTitle &&
    person.jobArea &&
    person.educationLevel &&
    Array.isArray(person.educationFields) &&
    Array.isArray(person.universities) &&
    Array.isArray(person.educationCountries) &&
    Array.isArray(person.languages) &&
    Array.isArray(person.interests) &&
    person.personalityType &&
    typeof person.careerGoal === "string"
  );
}

// Validering för utställare
function isValidExhibitor(exhibitor) {
  return (
    exhibitor.firstName &&
    exhibitor.lastName &&
    exhibitor.company &&
    exhibitor.mainField &&
    exhibitor.jobArea &&
    exhibitor.jobTitle &&
    exhibitor.educationLevel &&
    Array.isArray(exhibitor.educationFields) &&
    Array.isArray(exhibitor.universities) &&
    Array.isArray(exhibitor.educationCountries) &&
    Array.isArray(exhibitor.languages) &&
    Array.isArray(exhibitor.interests) &&
    exhibitor.personalityType &&
    typeof exhibitor.careerGoal === "string"
  );
}

// Spara person
app.post('/api/people', (req, res) => {
  const person = req.body;
  if (!isValidPerson(person)) {
    return res.status(400).json({ error: 'Alla fält måste vara ifyllda för person' });
  }
  const people = readJsonFile('people.json');
  people.push(person);
  writeJsonFile('people.json', people);
  res.status(201).json({ message: 'Person saved' });
});

// Spara utställare
app.post('/api/exhibitors', (req, res) => {
  const exhibitor = req.body;
  if (!isValidExhibitor(exhibitor)) {
    return res.status(400).json({ error: 'Alla fält måste vara ifyllda för utställare' });
  }
  const exhibitors = readJsonFile('exhibitors.json');
  exhibitors.push(exhibitor);
  writeJsonFile('exhibitors.json', exhibitors);
  res.status(201).json({ message: 'Exhibitor saved' });
});

// Hämta alla personer
app.get('/api/people', (req, res) => {
  const people = readJsonFile('people.json');
  res.json(people);
});

// Hämta alla utställare
app.get('/api/exhibitors', (req, res) => {
  const exhibitors = readJsonFile('exhibitors.json');
  res.json(exhibitors);
});

// Hämta matchningar
app.get('/api/matches', (req, res) => {
  exec('python3 matcher.py', (error, stdout, stderr) => {
    if (error || stderr) {
      console.error(error || stderr);
      return res.status(500).json({ error: 'Fel vid körning av matcher.py' });
    }
    try {
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (e) {
      res.status(500).json({ error: 'Fel vid tolkning av resultat från matcher.py' });
    }
  });
});

// API för parameterfiler
app.get('/api/parameters/:param', (req, res) => {
  const param = req.params.param;
  const file = path.join(__dirname, 'parameters', `${param}.json`);
  if (fs.existsSync(file)) {
    res.json(JSON.parse(fs.readFileSync(file)));
  } else {
    res.status(404).json({ error: "Parameter not found" });
  }
});

// Spara person till me.json
app.post('/api/me', (req, res) => {
  fs.writeFileSync('me.json', JSON.stringify([req.body]));
  res.json({ status: "saved" });
});

// Matcha me.json mot exhibitors.json
app.get('/api/me/matches', (req, res) => {
  exec('python3 matcher.py me.json exhibitors.json parameters/job_titles.json', (err, stdout) => {
    if (err) return res.status(500).json({ error: "Matchning misslyckades" });
    res.json(JSON.parse(stdout)[0]); // Endast första personen i me.json
  });
});

// Rensa me.json
app.delete('/api/me', (req, res) => {
  if (fs.existsSync('me.json')) fs.unlinkSync('me.json');
  res.json({ status: "deleted" });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});