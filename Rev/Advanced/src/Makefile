SRC_DIRECTORY=.
SERVER_NAME=server
SERVER_GO_SOURCE=server.go

CLIENT_NAME=dropper
CLIENT_GO_SOURCE=dropper.go

DATES_FILE=dates.txt
SAMPLES_DIR=samples
ZIP_FILE=droppers.zip

.PHONY: test build launch run generate_samples

test: build
	cd $(SRC_DIRECTORY) && go test -v ./...

build: 
	go build -gcflags "all=-N -l" -ldflags="" -o $(CLIENT_NAME) $(SRC_DIRECTORY)/client/$(CLIENT_GO_SOURCE)
	go build -gcflags "all=-N -l" -ldflags="" -o $(SERVER_NAME) $(SRC_DIRECTORY)/server/$(SERVER_GO_SOURCE)

launch:
	./$(SERVER_NAME) &

run: 
	./$(CLIENT_NAME)

generate_samples: $(DATES_FILE)
	@mkdir -p $(SAMPLES_DIR)
	@rm -f $(ZIP_FILE)
	@while read date; do \
		echo "Generating sample for $$date"; \
		go run generate_dropper.go $$date; \
		go build -o $(SAMPLES_DIR)/dropper_$$date $(SRC_DIRECTORY)/client/$(CLIENT_GO_SOURCE); \
		random_flag="BarSides{RANDOM_FLAG_$$date}"; \
		CTF_FLAG="$$random_flag" CTF_DATE="$$date" CTF_PORT="8999" go run $(SRC_DIRECTORY)/server/$(SERVER_GO_SOURCE) -output $(SAMPLES_DIR)/payload_$$date.bin; \
	done < $(DATES_FILE)
	@cd $(SAMPLES_DIR) && zip ../$(ZIP_FILE) dropper_* payload_*.bin
	@echo "Samples and payloads generated and zipped in $(ZIP_FILE)"

$(DATES_FILE):
	@echo "Please create a $(DATES_FILE) with one date per line in YYYYMMDD format."
	@exit 1