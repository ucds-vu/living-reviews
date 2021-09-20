from imports import *
import templates.tags as tags
from classes.statement import Statement
import settings

class Paper:
    def __init__(self, doi):
        self.statements = []
        self.studies = []
        self.doi = doi
        if "No-DOI" in self.doi or "arxiv" in self.doi:
            doi_number = self.doi[7:]
            if (len(doi_number) > 1):
                self.doi = settings.newNoDOi[:-(len(doi_number) - 1)] + doi_number
            else:
                self.doi = settings.newNoDOi + doi_number
            self.doiPresent = 0
        else:
            self.doiPresent = 1
        self.identifier = self.doi.split("/")[-1]

    def add_statement(self, line):
        newStatement = Statement(line[2], line[1])
        self.statements.append(newStatement)
        for study in self.studies:
            if study.presentsStudy == line[1]:
                study.add_statement(newStatement)

    def add_study(self, study):
        self.studies.append(study)


    def generateNanopub(self, date, file):
        template = open("./templates/paper-template.trig", "r")
        templateContent = template.read()
        newContent = ""
        positions = []
        for i in range(len(tags.paperTags)):
            positions.append(templateContent.index(tags.paperTags[i]))

        newContent = templateContent[:positions[0]] + settings.paperURI + self.identifier
        newContent += templateContent[positions[0] + len(tags.paperTags[0]): positions[1]]
        if self.doiPresent == 1:
            newContent += "<" + self.doi + ">"
            if  self.doi == "https://doi.org/10.1177%2F2056305115610141":
                newContent += " a fabio:ReviewArticle;\n\t"
            else:
                newContent += templateContent[positions[1] + len(tags.paperTags[1]): positions[2]]
        else:
            newContent += ":paper"
            newContent += templateContent[positions[1] + len(tags.paperTags[1]): positions[2]]
        for statement in self.statements:
            if len(self.studies) == 0 and statement == self.statements[-1]:
                newContent += "hycl:claims <https://purl.org/aida/" + statement.statement + ">.\n\t"
            else:
                newContent += "hycl:claims <https://purl.org/aida/" + statement.statement + ">;\n\t"

        for studyNumber in range(len(self.studies)):
            if studyNumber == len(self.studies) -1:
                newContent += "cdop:study <" + settings.studyURI + self.identifier + "/" + self.studies[studyNumber].presentsStudy + "/study>."
            else:
                newContent += "cdop:study <" + settings.studyURI + self.identifier + "/" + self.studies[studyNumber].presentsStudy + "/study>;\n\t"
        newContent += templateContent[positions[2] + len(tags.paperTags[2]): positions[3]]
        newContent += self.doi
        newContent += templateContent[positions[3] + len(tags.paperTags[3]): positions[4]]
        newContent += date
        newContent += templateContent[positions[4] + len(tags.paperTags[4]): ]

        file.write(newContent + "\n\n\n")

    def generateDoiNanopub(self, date, file):
        template = open("./templates/doi-template.trig", "r")
        templateContent = template.read()
        contentDoi = open("./doi/" + self.identifier + ".ttl")
        doiContent = contentDoi.read()
        newContent = ""
        positions = []
        for i in range(len(tags.doiTags)):
            positions.append(templateContent.index(tags.doiTags[i]))

        newContent = templateContent[:positions[0]] + settings.doiURI + self.identifier
        newContent += templateContent[positions[0] + len(tags.doiTags[0]): positions[1]]
        newContent += doiContent
        newContent += templateContent[positions[1] + len(tags.doiTags[1]): positions[2]]
        newContent += self.doi
        newContent += templateContent[positions[2] + len(tags.doiTags[2]): positions[3]]
        newContent += date
        newContent += templateContent[positions[3] + len(tags.doiTags[3]):]
        file.write(newContent + "\n\n\n")
