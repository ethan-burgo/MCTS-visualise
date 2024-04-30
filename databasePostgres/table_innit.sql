-- STEP 1:
INSERT INTO "MCTS_visualise"."Execution" (exe_id, title, starttime, endtime, resultdes)
VALUES ('0', '0', '0', '0', '0');

-- STEP 2
INSERT INTO "MCTS_visualise"."Node" (node_id, parent_id, execution_id, chosen, move_, childern, value_, visits)
VALUES ('0', '0', '0', 1, '0', '0', 0, 0);