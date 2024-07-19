const express = require('express');
const app = express();
const cors = require('cors');
app.use(cors()); // for cross origin
app.use(express.json()); //for res.json (if im not wrong)

const { attachDatabasePool } = require('./db.js');
app.use(attachDatabasePool); //usage example: await req.db.query('SELECT 1');

app.get('/qp-search', async (req, res) => {
  const {q} = req.query;
  console.log(q);
  try {
    const qp_list = await req.db.query('SELECT * FROM files WHERE file_name ILIKE $1', [`%${q}%`]);
    console.log(qp_list.rows);
    if(qp_list.rowCount == 0) {
      return res.status(401).send("No files found.");
    } else {
      return res.status(200).send(qp_list.rows);
    }
  } catch(e) {
    console.log(e);
    return res.status(500).send("Internal server error");
  }
});

app.get('/qp/branches', async (req,res) => {
  try {
    const branch_list = await req.db.query(`SELECT
    id, CONCAT(type, ' of ', name, ' [', tag, ']') AS branch FROM branch ORDER BY type LIMIT 10;`);
    if(branch_list.rowCount === 0) {
      return res.status(404).send("No branches defined");
    } else {
      return res.status(200).send(branch_list.rows);
    }
  } catch (e) {
    console.log(e);
    return res.status(500).send("Internal server error");
  }
});

app.get('/qp/subjects', async (req, res) => {
  const { branchId, scheme, semester } = req.query;
  console.log(branchId, scheme, semester)
  let query = 'SELECT DISTINCT subject_name, subject_code, paper_id, m_code FROM paper_ids WHERE branch_id = $1 AND scheme = $2 AND semester = $3 LIMIT 3';
  const params = [branchId, scheme, semester];

  try {
    const subjects = await req.db.query(query, params);
    if (subjects.rowCount === 0) {
      return res.status(404).send('No subjects found');
    } else {
      return res.status(200).send(subjects.rows);
    }
  } catch (error) {
    console.log(error);
    return res.status(500).send('Internal server error');
  }
});
app.get('/', async (req, res) => {
  return res.send('Yep, this api works.');
});
// Endpoint to search for exam papers based on paper_id, m_code, and subject_code
app.get('/qp/search-papers', async (req, res) => {
  const { paperId, mCode, subjectCode } = req.query;
  const queryParams = [`%${paperId}%`, `%${mCode}%`, `%${subjectCode}%`];

  let query = 'SELECT * FROM files WHERE file_name ILIKE $1 OR file_name ILIKE $2 OR file_name ILIKE $3 LIMIT 10';
  const params = queryParams;

  try {
    const examPapers = await req.db.query(query, params);
    if (examPapers.rowCount === 0) {
      return res.status(404).send('No exam papers found');
    } else {
      return res.status(200).send(examPapers.rows);
    }
  } catch (error) {
    console.log(error);
    return res.status(500).send('Internal server error');
  }
});

const PORT = process.env.APP_PORT
// running the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});
