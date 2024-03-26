
-- Execution table
CREATE TABLE "MCTS_visualise"."Execution" (
    id VARCHAR(255) PRIMARY KEY,
    Title VARCHAR(255),
	StartTime VARCHAR(255),
	EndTime VARCHAR(255),
	ResultDes VARCHAR(255)
);

-- State table
CREATE TABLE "MCTS_visualise"."State_tb" (
	id SERIAL PRIMARY KEY,
	current_state JSON,
    node_id VARCHAR(255),
    CONSTRAINT fk_node_id
	FOREIGN KEY (node_id)
	REFERENCES "MCTS_visualise"."Node"(id)
);

-- Node table
CREATE TABLE "MCTS_visualise"."Node" (
    id VARCHAR(255) PRIMARY KEY,
    parent_id VARCHAR(255),
	execution_id VARCHAR(255),
	CONSTRAINT fk_execution_id
	FOREIGN KEY (execution_id)
	REFERENCES "MCTS_visualise"."Execution"(id),
	chosen INT,
	move_ VARCHAR(255),
	childern VARCHAR(1000),
	value_ INT,
	visits INT
);

ALTER TABLE "MCTS_visualise"."Node"
ADD CONSTRAINT fk_parent_id
FOREIGN KEY (parent_id) 
REFERENCES "MCTS_visualise"."Node"(id);