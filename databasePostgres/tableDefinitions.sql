
-- Execution table
CREATE TABLE "MCTS_visualise"."Execution" (
    id SERIAL PRIMARY KEY,
    Title VARCHAR(255),
	StartTime VARCHAR(255),
	EndTime VARCHAR(255),
	ResultDes VARCHAR(255)
);

-- State table
CREATE TABLE "MCTS_visualise"."State_tb" (
	id SERIAL PRIMARY KEY,
	current_state JSON
);

-- Node table
CREATE TABLE "MCTS_visualise"."Node" (
    id VARCHAR(255) PRIMARY KEY,
    parent_id VARCHAR(255),
	execution_id INT,
	CONSTRAINT fk_execution_id
	FOREIGN KEY (execution_id)
	REFERENCES "MCTS_visualise"."Execution"(id),
	state_id INT,
	CONSTRAINT fk_state_id
	FOREIGN KEY (state_id)
	REFERENCES "MCTS_visualise"."State_tb"(id),
	chosen INT,
	move_ VARCHAR(255),
	childern VARCHAR(100)[],
	value_ INT,
	visits INT
);

ALTER TABLE "MCTS_visualise"."Node"
ADD CONSTRAINT fk_parent_id
FOREIGN KEY (parent_id) 
REFERENCES "MCTS_visualise"."Node"(id);