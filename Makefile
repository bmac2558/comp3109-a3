ANTLR_JAR=antlr-3.1.3.jar
BUILD_DIR=build
GRAMMAR_FILE=VPL.g
PYTREE_DIR=a3tree

.PHONY: all clean compile

all: ${BUILD_DIR}/__init__.py

${BUILD_DIR}: ${GRAMMAR_FILE}
	@mkdir -p ${BUILD_DIR}
	@touch ${BUILD_DIR}

${ANTLR_JAR}:
	wget http://www.antlr.org/download/${ANTLR_JAR}

${BUILD_DIR}/__init__.py: ${ANTLR_JAR} ${BUILD_DIR} ${GRAMMAR_FILE}
	java -cp ${ANTLR_JAR} org.antlr.Tool -o ${BUILD_DIR} ${GRAMMAR_FILE}
	@touch ${BUILD_DIR}/__init__.py

test: all
	bash test.sh

clean:
	rm -r a3 ${BUILD_DIR} *.s *.pyc ${PYTREE_DIR}/*.pyc
