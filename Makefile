ANTLR_JAR=antlr-3.1.2.jar
BUILD_DIR=build
GRAMMAR_FILE=VPL.g
PYTREE_DIR=a3tree

all: ${BUILD_DIR}/__init__.py ${ANTLR_JAR}

${BUILD_DIR}: ${GRAMMAR_FILE}
	@mkdir -p ${BUILD_DIR}
	@touch ${BUILD_DIR}/__init__.py
	@touch ${BUILD_DIR}

${BUILD_DIR}/__init__.py: ${ANTLR_JAR} ${BUILD_DIR} ${GRAMMAR_FILE}
	java -cp ${ANTLR_JAR} org.antlr.Tool -o ${BUILD_DIR} ${GRAMMAR_FILE}
	@touch ${BUILD_DIR}/__init__.py

${ANTLR_JAR}:
	wget http://antlr.org/path/goes/here/${ANTLR_JAR}

clean:
	rm -r a3 ${BUILD_DIR} *.s *.pyc ${PYTREE_DIR}/*.pyc
