
-- Execution table (STEP 1)
CREATE TABLE "MCTS_visualise"."Execution" (
    exe_id VARCHAR(255) PRIMARY KEY,
    Title VARCHAR(255),
	StartTime VARCHAR(255),
	EndTime VARCHAR(255),
	ResultDes VARCHAR(255)
);

-- Node table (STEP 2)
CREATE TABLE "MCTS_visualise"."Node" (
    node_id VARCHAR(255) PRIMARY KEY,
    parent_id VARCHAR(255),
	execution_id VARCHAR(255),
	CONSTRAINT fk_execution_id
	FOREIGN KEY (execution_id)
	REFERENCES "MCTS_visualise"."Execution"(exe_id),
	chosen INT,
	move_ VARCHAR(255),
	childern VARCHAR(1000),
	value_ INT,
	visits INT
);

-- Add self referencing fk (STEP 3)
ALTER TABLE "MCTS_visualise"."Node"
ADD CONSTRAINT fk_parent_id
FOREIGN KEY (parent_id) 
REFERENCES "MCTS_visualise"."Node"(node_id);


-- State table (STEP 4)
CREATE TABLE "MCTS_visualise"."State_tb" (
	state_id SERIAL PRIMARY KEY,
	current_state JSONB,
    node_id_s VARCHAR(255),
    CONSTRAINT fk_node_id
	FOREIGN KEY (node_id_s)
	REFERENCES "MCTS_visualise"."Node"(node_id)
);
