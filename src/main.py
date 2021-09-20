from imports import *
import settings
def usage():
    print("Options:\n \
    -d / --doi Get DOIs to download\n")

def preprocess(content):
    contentPerLine = content.splitlines()
    contentSeparated = []
    for line in contentPerLine:
        contentSeparated.append(line.split(";"))
    return contentSeparated

def main():
    doi = False
    settings.init()
    try:
        options, remainder = getopt.getopt(sys.argv[1:], "d", ['doi'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-d', '--doi'):
            doi = True
        else:
            sys.stderr.write("ERROR: Unhandled option entered\n")
            sys.exit(2)

    # Process studies
    studyFD= open("../data/Study.csv")
    studyContent = studyFD.read()
    preprocessedStudies = preprocess(studyContent)
    studyObjects = []
    paperObjects = []
    count = 0
    for studyNumber in range(1, len(preprocessedStudies)):
        currentStudy = Study(preprocessedStudies[studyNumber])
        studyObjects.append(currentStudy)
        count+= 1
        if preprocessedStudies[studyNumber][0] == preprocessedStudies[studyNumber -1][0]:
            paperObjects[-1].add_study(currentStudy)
        else:
            paperObjects.append(Paper(preprocessedStudies[studyNumber][0]))
            paperObjects[-1].add_study(currentStudy)

    paperFD = open("../data/Papers_in_table.csv")
    paperContent = paperFD.read()
    preprocessedPapers = preprocess(paperContent)
    for paper in preprocessedPapers[1:]:
        present = 0
        for paperPresent in paperObjects:
            if paper[0] == paperPresent.doi:
                present = 1
                break
            elif "No-DOI" in paper[0]:
                doi_number = paper[0][7:]
                if (len(doi_number) > 1):
                    doi_uri = settings.newNoDOi[:-(len(doi_number) - 1)] + doi_number
                else:
                    doi_uri = settings.newNoDOi + doi_number
                if doi_uri == paperPresent.doi:
                    present = 1
                    break
        if present == 0:
            paperObjects.append(Paper(paper[0]))



    #Process statements
    statementsFD = open("../data/Statements.csv")
    statementContent = statementsFD.read()
    preprocessedStatements = preprocess(statementContent)

    # Quite slow make sure that they use the ordering
    for statementNumber in range(1, len(preprocessedStatements)):
        for paper in paperObjects:
            if paper.doi == preprocessedStatements[statementNumber][0]:
                paper.add_statement(preprocessedStatements[statementNumber])


    # Process relations
    relationFD= open("../data/Relations.csv")
    relationContent = relationFD.read()
    preprocessedRelations = preprocess(relationContent)
    relationObjects = []
    for relationNumber in range(1, len(preprocessedRelations)):
        relationObjects.append(Relation(preprocessedRelations[relationNumber], relationNumber))

    # Process No Doi
    NoDoiFD= open("../data/No-DOI-Study.csv")
    NoDoiContent = NoDoiFD.read()
    preprocessedNoDoi = preprocess(NoDoiContent)

    # ReviewPaper
    reviewPaperFD = open("../data/Unique_DOI.csv")
    reviewPaperContent = reviewPaperFD.read()
    preprocessedReview = preprocess(reviewPaperContent)
    reviewPapers = []
    reviewPapers.append(ReviewPaper(preprocessedReview[1]))
    for paperNum in range(2, len(preprocessedReview)):
        if preprocessedReview[paperNum][0] == preprocessedReview[paperNum -1][0]:
            reviewPapers[-1].add_doi(preprocessedReview[paperNum][1])
        else:
            reviewPapers.append(ReviewPaper(preprocessedReview[paperNum]))


    #Generate nanopubs
    os.chdir("../../")
    try:
        currentDate = subprocess.check_output(['./np', 'now'])
        currentDate = currentDate.decode('utf-8')[:-1]
    except:
        sys.stderr.write("ERROR: Path to nanopublication library is not found or working\n")
        sys.exit(1)

    os.chdir("./living-reviews/src")

    relationNanopubs = open("../np/relations.trig", "w+")
    tags.relationTag()
    for relationObject in relationObjects:
        relationObject.generateNanopub(currentDate, relationNanopubs)

    studyNanopubs = open("../np/studies.trig", "w+")
    tags.studyTag()
    for studyObject in studyObjects:
        studyObject.generateNanopub(currentDate, studyNanopubs)

    paperNanopubs = open("../np/papers.trig", "w+")
    doiNanopubs = open("../np/dois.trig", "w+")
    tags.paperTag()
    tags.doiTag()

    # subprocess.check_output(['sh', 'doi.sh', paperObjects[0].doi])
    # paperObjects[0].generateDoiNanopub(currentDate, doiNanopubs)

    if doi:
        print("GETTING DOIs\n")
        for paperObject in paperObjects:
            filePath = "./doi/" + paperObject.identifier + ".ttl"
            if paperObject.doiPresent == 1 and not os.path.exists(filePath):
                toPrint = paperObject.doi + " " + paperObject.identifier
                print(toPrint)
        sys.exit(0)


    for paperObject in paperObjects:
        paperObject.generateNanopub(currentDate, paperNanopubs)
        filePath = "./doi/" + paperObject.identifier + ".ttl"
        if paperObject.doiPresent == 1 and os.path.exists(filePath):
            paperObject.generateDoiNanopub(currentDate, doiNanopubs)

    for noDOI in range(1, len(preprocessedNoDoi)):
        generateNoDoiNanopub(preprocessedNoDoi[noDOI], currentDate, doiNanopubs)

    reviewNanopubs = open("../np/reviews.trig", "w+")
    tags.reviewTag()
    for review in reviewPapers:
        review.generateNanopub(currentDate, reviewNanopubs)

if __name__ == "__main__":
    main()
