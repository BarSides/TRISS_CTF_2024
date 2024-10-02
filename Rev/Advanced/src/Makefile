SRC_DIRECTORY=.
SERVER_NAME=server
SERVER_GO_SOURCE=server.go

CLIENT_NAME=dropper
CLIENT_GO_SOURCE=dropper.go

.PHONY: test build launch run

test: build
	cd $(SRC_DIRECTORY) && go test -v ./...

build: 
	go build -gcflags "all=-N -l" -ldflags="" -o $(CLIENT_NAME) $(SRC_DIRECTORY)/client/$(CLIENT_GO_SOURCE)
	go build -gcflags "all=-N -l" -ldflags="" -o $(SERVER_NAME) $(SRC_DIRECTORY)/server/$(SERVER_GO_SOURCE)

launch:
	./$(SERVER_NAME) &

run: 
	./$(CLIENT_NAME)