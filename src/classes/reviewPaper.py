from imports import *
import templates.tags as tags
import settings
class ReviewPaper:

    def __init__(self, line):
        self.reviewPaperDoi = line[0]
        self.identifier = self.reviewPaperDoi.split("/")[-1]
        self.reviewDois = []
        if "No-DOI" not in line[1]:
            self.reviewDois.append(line[1])
        else:
            doi_number = line[1][7:]
            if (len(doi_number) > 1):
                newDOI = settings.newNoDOi[:-(len(doi_number) - 1)] + doi_number
            else:
                newDOI = settings.newNoDOi + doi_number
            self.reviewDois.append(newDOI)

    def add_doi(self, doi):
        if "No-DOI" not in doi:
            self.reviewDois.append(doi)
        else:
            doi_number = doi[7:]
            if (len(doi_number) > 1):
                newDOI = settings.newNoDOi[:-(len(doi_number) - 1)] + doi_number
            else:
                newDOI= settings.newNoDOi + doi_number
            self.reviewDois.append(newDOI)

    def generateNanopub(self, date, file):
        template = open("./templates/review-paper-template.trig", "r")
        templateContent = template.read()
        newContent = ""
        positions = []
        for i in range(len(tags.reviewTags)):
            positions.append(templateContent.index(tags.reviewTags[i]))

        newContent = templateContent[:positions[0]] + settings.reviewPaperURI + self.identifier
        newContent += templateContent[positions[0] + len(tags.reviewTags[0]): positions[1]]
        newContent += self.reviewPaperDoi
        newContent += templateContent[positions[1] + len(tags.reviewTags[1]): positions[2]]
        for doi in self.reviewDois:
            if doi == "https://doi.org/10.1177%2F2056305115610141":
                continue
            if doi == self.reviewDois[-1]:
                newContent += "cito:reviews <" + doi + ">."
            else:
                newContent += "cito:reviews <" + doi + ">;\n\t\t"
        newContent += templateContent[positions[2] + len(tags.reviewTags[2]): positions[3]]
        newContent += self.reviewPaperDoi
        newContent += templateContent[positions[3] + len(tags.reviewTags[3]): positions[4]]
        newContent += date
        newContent += templateContent[positions[4] + len(tags.reviewTags[4]): ]
        file.write(newContent + "\n\n\n")
