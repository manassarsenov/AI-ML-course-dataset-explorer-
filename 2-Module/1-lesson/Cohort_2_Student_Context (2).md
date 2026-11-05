# AI/ML Fundamentals | Cohort 2
## Student learning-space reference

**Edition:** 1.0, prepared 12 October 2026 for mentor review.  
**Basis:** Cohort 2 delivery version 2.0, dated 20 September 2026.  
**Status:** A new student-facing summary, not a replacement for an issued assignment, the official curriculum or the assessment policy. Later mentor-issued lesson materials may refine the activity.

## 1. What this course is for

Learn enough machine learning to understand a problem, work with data, train and evaluate models, and explain a reproducible result. Use AI early, but keep your own decisions and understanding visible.

The program contains M1–M8 and the separate FINAL module, **Capstone Showcase and Career Launch**, with lessons F1–F6. There are 53 teaching sessions: 47 in M1–M8 and six in FINAL. Labs are already included. Midterm, Final Exam and the separate Capstone Defense follow the announced assessment arrangements; this summary does not set their dates.

Nikita Terentev is the technical mentor. Darya Argentova is the assistant and visual presenter. The original source materials were authored by Nikita Terentev and Saidazam Saidov.

## 2. The learning route

| Module | Official module name | Main focus and evidence of learning |
|---|---|---|
| M1 | AI and ML Foundations | Frame a problem, ask a browser assistant a useful question, refine it and check its answer against a source. Explain a new example yourself. |
| M2 | Python and Data Foundations | Run and change short code in Colab. Work with arrays, tables, charts and small calculations. Build a small agent-assisted application from a starter, make a meaningful change and check the result. |
| M3 | Data Preparation and Feature Engineering | Understand cleaning, transformations, features and evaluation splits. Give an agent the real files, useful project context and clear boundaries. Check that preprocessing does not leak information. |
| M4 | Supervised Learning | Train and compare models, interpret metrics, run controlled experiments and fix a confirmed error. Explain the baseline, model choice and origin of each reported result. |
| M5 | Unsupervised Learning | Explore clusters, reduced representations and anomalies. Interpret only what the data supports. Connect a saved model and its preprocessing to a simple demo and compare its output with the notebook. |
| M6 | Neural Networks and Deep Learning | Understand basic neural-network behavior, inspect learning curves and change one experimental factor at a time. Use one prepared Skill and verify that its procedure actually ran. |
| M7 | NLP and Computer Vision | Work with text, images and pretrained components. Check model sources and input/output formats. Distinguish inference from training or fine-tuning, and repair small pipeline errors. |
| M8 | Capstone Project Studio | Develop one individual project: scope, repository, data, modeling, evaluation, artifacts, demo and evidence. Save a working checkpoint and identify remaining gaps. |
| FINAL | Capstone Showcase and Career Launch | Complete and present the same project: diagnose gaps, specify a bounded change, check and repair it, prepare a truthful showcase and career materials, and rehearse the defense. |

This route does not mean every topic requires a new tool. Browser AI is used first. Colab remains the main visible ML environment. One coding agent is sufficient; Codex and Antigravity are examples of alternatives, not two mandatory courses. A subscription, paid API, MCP server or multi-agent setup is not a prerequisite.

## 3. How AI should help you

For a new concept, ask for a clear explanation, a tiny example and a chance to apply the idea. You can ask in your preferred language while keeping the course's English technical terms.

For a learning exercise, share your attempt or the exact point where you are stuck. A useful helper gives enough support to let you take the next step, instead of filling in the whole answer sheet.

For an activity that permits AI-assisted coding, the assistant may write or repair code. You do not need to hand-type every routine line. You still decide what the code should do, inspect the relevant change, run or verify it in the required environment, and explain its result. Follow any task-specific requirement for your own change or calculation.

Examples from the course route:

- In M1, an explanation or a practice question does not replace your own scenario classification and justification.
- In M2, help with a function or a small application must lead to your own observable run and a checked change. A chat reply does not automatically update your Colab notebook.
- In M3–M7, an agent may support data work, experiments and debugging within the task's boundaries. Actual outputs, valid comparisons and your explanation remain necessary.
- In FINAL F2, prepare the change specification and inspect with a Skill; do not change application/model behavior yet. FINAL F3 executes the agreed checks and permits a minimal, verified repair.

An independent no-AI test, diagnostic explanation or live defense answer must remain your own. Rehearsal and revision outside that assessment may use AI within the mentor's rules. An AI helper cannot grant an exception to an issued rule.

## 4. What counts as evidence

**Prepared** means code, a plan or a check exists. **Executed** means it actually ran in a stated environment. **Verified** means the observed result was checked against a clear expectation. **Blocked** means a missing file, access, dependency or other obstacle prevented the action.

A generated test file is not a passed test. A stored notebook output may be from an earlier run. An agent's run in another environment is not automatically your own successful Colab run. Label each accurately.

For a numerical claim, retain the input, calculation or run, actual output and interpretation. Do not invent a better score or hide a failed experiment. A bad result can still be useful evidence when its cause and limits are explained.

Learned preprocessing must be fitted on training data, not on the protected test set. Do not use repeated test-set feedback to select or tune a model. Keep comparisons fair and explain relevant errors. Software checks and ML evaluation answer different questions; neither replaces the other.

Keep explanations separate from unsupported assumptions: a cluster label is not a person's motive, an anomaly is not proof of wrongdoing, and correlation is not evidence of a causal effect by itself.

## 5. Capstone boundaries

Capstone projects are individual. The **Individual Project Track** and **Field-Based Scenario Track** use the same rubric.

The core expectations include a trained or fine-tuned model, evaluation on unseen data, a working end-to-end reproducible demo, documentation, and an independent defense with questions. The official rubric also specifies deliverables, baseline and modeling comparisons, experiment records, error analysis, reproducibility and responsible-AI evidence. This paragraph is a summary, not the complete checklist.

An application that only calls an external AI API does not satisfy the model-training requirement. A reproducible Colab demo is a valid route. An API, Docker, public hosting, a website or a Skill is not an extra universal condition for passing Capstone.

M8C6 saves a working checkpoint. FINAL F6 checks the version prepared for submission before the official deadline. Neither lesson automatically changes that deadline or authorizes late additions.

Use the official rubric, implementation helper and submission template when they are issued. The submission file and repository access must follow the actual LMS instructions. Do not infer submission requirements from old examples.

## 6. Sources and disagreements

For **grading, deadlines, AI permissions and required outputs**, consult the official rule and the actual issued assignment. For **the current activity**, use current mentor-issued student materials. Use this summary for orientation, not to override those sources.

If sources disagree, identify the documents and the conflicting statements. Ask the mentor rather than silently choosing an easier rule. If a technical statement appears wrong, explain the concern and check reliable technical evidence; do not reproduce a factual error only because it appeared in a handout.

Use student-facing notes, the current assignment, the relevant starter code and a safe data description. Do not treat instructor answer keys, another student's submission, archival reference examples or an old resource list as current task instructions.

A filename in this reference does not prove that an AI can open that file. Use only sources actually available in the current tool. For an unavailable source, provide its relevant section or ask for general conceptual help without claiming source-specific certainty.

## 7. Optional context for a new chat or tool

You may paste a short message such as:

```text
Current lesson/topic: [your actual topic]
Goal: [what you want to understand or do]
Relevant material: [attached file and section, or pasted code]
What I tried: [your attempt, or "not started"]
Actual result/error: [real output, or "not run"]
Allowed changes: [scope, or "explain only; do not edit"]
Help me take one meaningful next step.
```

This is a convenience, not extra homework or a required prompt log. Do not include credentials or private records. When your Capstone already has a `PROJECT_STATUS.md` or another agreed status note, reuse it rather than maintaining a second competing record. Do not assume that a browser assistant and a coding agent share history or files.

## 8. Preparation sources

The following documents were used to prepare this reference. They are provenance records, **not a claim that these files are attached to the student's space**. Request the actual issued document for a source-specific question.

- `01_Expanded_Curriculum_Cohort_2(2).docx`: learning route; AI workflow and boundaries; M2C1, M2C6, M3C4; M8 and FINAL lesson cards.
- `02_Course_Map_Cohort_2(2).docx`: module sequence, student evidence and repeated use of AI skills.
- `DOC_1_overview(2).md`: current Cohort 2 structure, source priorities and module boundaries. Its historical sections are not a current student schedule.
- `DOC_4_all_assignments(2).md`: current practice, permitted AI role and relationship to the original LMS assignments.
- `Capstone_Project_Evaluation_Criteria_AI_ML_Fundamentals(2).docx`: policy v1.1, project format, requirements, deliverables and integrity rules. Official rubric authors: Nikita Terentev and Saidazam Saidov.
- `Методология_подготовки_уроков_FINAL_Module(2).md`: evidence rules, F2/F3 distinction and the M8-to-FINAL boundary.

Original source documents, author names, assessment policy and LMS instructions have not been edited by this summary.
