from imports import *
import templates.tags as tags
import settings
class Relation:
    def __init__(self, line, number):
        self.relationNumber = number
        self.statement1 = line[0].replace(" ", "+")
        self.paper1 = line[1]
        self.statement2 = line[2].replace(" ","+")
        self.paper2 = line[3]
        if line[4] == "providesCounterevidenceFor":
            self.relation = "llr:providesCounterevidenceFor"
        elif line[4] == "hasMoreSpecificMeaning":
            self.relation = "hycl:hasMoreSpecificMeaningThan";
        else:
            self.relation = "hycl:" + line[4]
        self.statement1 = self.statement1.replace('"','')
        self.statement2 = self.statement2.replace('"','')

    def generateNanopub(self, date, file):
        template = open("./templates/relation-template.trig", "r")
        templateContent = template.read()
        newContent = ""
        positions = []
        for i in range(len(tags.relationTags)):
            positions.append(templateContent.index(tags.relationTags[i]))
        newContent = templateContent[:positions[0]] + settings.relationURI +str(self.relationNumber)
        newContent += templateContent[positions[0] + len(tags.relationTags[0]): positions[1]]
        newContent += self.statement1
        newContent += templateContent[positions[1] + len(tags.relationTags[1]): positions[2]]
        newContent += self.relation
        newContent += templateContent[positions[2] + len(tags.relationTags[2]): positions[3]]
        newContent += self.statement2
        newContent += templateContent[positions[3] + len(tags.relationTags[3]): positions[4]]
        newContent += date
        newContent += templateContent[positions[4] + len(tags.relationTags[4]):]

        file.write(newContent + "\n\n\n")
