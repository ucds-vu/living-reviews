from imports import *
import templates.tags as tags
from classes.statement import Statement
import settings

class Study:
    def __init__(self, line):
        self.statements = []
        self.doi = line[0]
        if "No-DOI" in self.doi or "arxiv" in self.doi:
            doi_number = self.doi[7:]
            if (len(doi_number) > 1):
                self.doi = settings.newNoDOi[:-(len(doi_number) - 1)] + doi_number
            else:
                self.doi = settings.newNoDOi + doi_number
        self.title = line[1]
        self.articleType = line[2]
        if line[3] == "USA":
            self.firstAuthorOrigin = "https://dbpedia.org/resource/United_States"
        elif line[3] == "United Kingdom":
            self.firstAuthorOrigin = "https://dbpedia.org/resource/United_Kingdom"
        elif line[3] == "South Afrika":
            self.firstAuthorOrigin = "https://dbpedia.org/resource/South_Africa"
        elif line[3] == "South Korea":
            self.firstAuthorOrigin = "https://dbpedia.org/resource/South_Korea"
        elif line[3] == "Unknown":
            self.firstAuthorOrigin = "Unknown"
        else:
            self.firstAuthorOrigin = "https://dbpedia.org/resource/" + line[3]
        self.landsOfFocus = []

        splitLands = line[4].split(", ")
        for land in splitLands:
            if land == "USA":
                self.landsOfFocus.append("<https://dbpedia.org/resource/United_States>")
            elif land == "United Kingdom":
                self.landsOfFocus.append("<https://dbpedia.org/resource/United_Kingdom>")
            elif land == "South Afrika":
                self.landsOfFocus.append("<https://dbpedia.org/resource/South_Africa>")
            elif land == "South Korea":
                self.landsOfFocus.append("<https://dbpedia.org/resource/South_Korea>")
            elif "Unknown" not in land:
                self.landsOfFocus.append("<https://dbpedia.org/resource/" + land + ">")

        self.landsOfDataCollection = []
        landOfDataCollection = line[5].split(", ")
        for land in landOfDataCollection:
            if land == "USA":
                self.landsOfDataCollection.append("<https://dbpedia.org/resource/United_States>")
            elif land == "United Kingdom":
                self.landsOfDataCollection.append("<https://dbpedia.org/resource/United_Kingdom>")
            elif land == "South Afrika":
                self.landsOfDataCollection.append("<https://dbpedia.org/resource/South_Africa>")
            elif land == "South Korea":
                self.landsOfDataCollection.append("<https://dbpedia.org/resource/South_Korea>")
            elif "Unknown" not in land:
                self.landsOfDataCollection.append("<https://dbpedia.org/resource/" + land + ">")
        self.socialMediaPlatform = line[6]
        self.theoreticalApproach = line[7]
        self.analysisType = line[8]
        self.methodStudy = line[9]
        self.studySize = line[10]
        self.primaryObject = line[11]
        self.presentsStudy = line[12]
        self.identifier = self.doi.split("/")[-1] + "/" + self.presentsStudy
        self.identifier.replace(" ", "")
        self.classes = []
        if "Unknown" not in self.analysisType:
            self.classes.append(self.analysisType.replace(" ", ""))
        if "Unknown" not in self.methodStudy:
            self.classes.append(self.methodStudy.replace(" ", ""))
        if "Unknown" not in self.articleType:
            self.classes.append(self.articleType.replace(" ", ""))

    def add_statement(self, statement):
        self.statements.append(statement)


    def generateNanopub(self, date, file):
        template = open("./templates/study-template.trig", "r")
        templateContent = template.read()
        newContent = ""
        positions = []
        for i in range(len(tags.studyTags)):
            positions.append(templateContent.index(tags.studyTags[i]))

        newContent = templateContent[:positions[0]] + settings.studyURI + self.identifier
        newContent += templateContent[positions[0] + len(tags.studyTags[0]): positions[1]]
        for classProperty in self.classes:
            newContent += "a llr:" + classProperty + ";\n\t"

        if len(self.landsOfFocus) > 0:
            for land in self.landsOfFocus:
                newContent += "llr:landOfFocus " + land + ";\n\t"

        if len(self.landsOfDataCollection) > 0:
            for land in self.landsOfDataCollection:
                newContent += "cdop:country " + land + ";\n\t"
        if "Unknown" not in self.studySize:
            newContent += "cdop:overall \"" + self.studySize + "\"^^xsd:string;\n\t"
        if "None" not in self.socialMediaPlatform:
            platforms = self.socialMediaPlatform.split(", ")
            for platform in platforms:
                if "Facebook" in platform:
                    link = "https://www.wikidata.org/wiki/Q355"
                elif "Twitter" in platform:
                    link = "https://www.wikidata.org/wiki/Q918"
                elif "Second Life" in platform:
                    link = "https://www.wikidata.org/wiki/Q106827"
                elif "Flickr" in platform:
                    link = "https://www.wikidata.org/wiki/Q103204"
                elif "Youtube" in platform:
                    link = "https://www.wikidata.org/wiki/Q866"
                elif "Foursquare" in platform:
                    link = "https://www.wikidata.org/wiki/Q51709" # company not specific platform
                elif "Digg" in platform:
                    link = "https://www.wikidata.org/wiki/Q270478"
                elif "GooglePlus" in platform:
                    link = "https://www.wikidata.org/wiki/Q356"
                elif "Reddit" in platform:
                    link = "https://www.wikidata.org/wiki/Q1136"
                elif "Instagram" in platform:
                    link = "https://www.wikidata.org/wiki/Q209330"
                elif "Sina Weibo" in platform:
                    link = "https://www.wikidata.org/wiki/Q92526"
                else:
                    print("Error no link for platform " + platform);
                    link = platform
                newContent += "llr:socialMediaPlatform <" + link + ">;\n\t"
        if "Unknown" not in self.theoreticalApproach:
            newContent += "llr:theoreticalApproach \"" + self.theoreticalApproach + "\"^^xsd:string;\n\t"
        if "Unknown" not in self.primaryObject:
            newContent += "llr:primaryObject \"" + self.primaryObject + "\"^^xsd:string;\n\t"

        for statement in self.statements:
            newContent += "llr:providesEvidenceFor <https://purl.org/aida/" + statement.statement + ">;\n\t"
        newContent += templateContent[positions[1] + len(tags.studyTags[1]): positions[2]]
        newContent += self.firstAuthorOrigin
        newContent += templateContent[positions[2] + len(tags.studyTags[2]): positions[3]]
        newContent += self.doi
        newContent += templateContent[positions[3] + len(tags.studyTags[3]): positions[4]]
        newContent += date
        newContent += templateContent[positions[4] + len(tags.studyTags[4]): ]

        file.write(newContent + "\n\n\n")
