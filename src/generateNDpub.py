from imports import *
import templates.tags as tags
import settings


def generateNoDoiNanopub(line, date, file):
    no_doi_prefix = "0000000000"
    title = line[1]
    doi_number = line[0][7:]
    identifier = no_doi_prefix[:-(len(doi_number) - 1)] + doi_number
    authors = line[2].split(" - ")
    journal = line[3]
    volume = line[4]
    year = line[5]
    template = open("./templates/doi-template.trig", "r")
    templateContent = template.read()

    if (len(doi_number) > 1):
        doi_found = settings.newNoDOi[:-(len(doi_number) - 1)] + doi_number
    else:
        doi_found = settings.newNoDOi + doi_number
    doi = "<" + settings.newNoDOi + doi_found + ">"

    newContent = ""
    positions = []
    for i in range(len(tags.doiTags)):
        positions.append(templateContent.index(tags.doiTags[i]))

    newContent = templateContent[:positions[0]] + settings.doiURI + identifier
    newContent += templateContent[positions[0] + len(tags.doiTags[0]): positions[1]]
    for author in authors:
        name_link = author.replace(" ", "-")
        name_link = name_link.replace('.', '')
        names = author.split(" ")
        newContent += "<" + settings.namespace + "crossref/contributor/" + name_link + "> a <http://xmlns.com/foaf/0.1/Person>;\n\t\t"
        newContent += "<http://xmlns.com/foaf/0.1/familyName> \"" + names[-1] + "\";\n\t\t"
        newContent += "<http://xmlns.com/foaf/0.1/givenName> \"" + names[0] + "\";\n\t\t"
        newContent += "<http://xmlns.com/foaf/0.1/name> \"" + author + "\".\n\n\t"

    if journal != "None":
        newContent += "<" + settings.namespace + "crossref/journal/" + journal.replace(' ', '-') + "> a <http://purl.org/ontology/bibo/Journal>;\n\t\t"
        newContent += "<http://purl.org/dc/terms/title> \"" + journal + "\".\n\n\t"

    newContent += doi + "\n\t\t"
    newContent += "<http://purl.org/dc/terms/date> \"" + year + "\";\n\t\t"
    newContent += "<http://purl.org/dc/terms/title> \"" + title.replace("\"", "''") + "\";\n\t\t"

    if journal != "None":
        newContent += "<http://purl.org/dc/terms/isPartOf> <" + settings.namespace + "crossref/journal/" + journal.replace(' ', '-') + ">;\n\t\t"
    if volume != "None":
        newContent += "<http://purl.org/ontology/bibo/volume> \"" + volume + "\";\n\t\t"
        newContent += "<http://prismstandard.org/namespaces/basic/2.1/volume> \"" + volume + "\";\n\t\t"
    newContent += "<http://purl.org/dc/terms/creator> "
    for author in authors:
        nameURL = author.replace(" ", "-")
        nameURL = nameURL.replace('.', '')
        newContent += "<" + settings.namespace + "crossref/contributor/" + nameURL + ">"
        if author == authors[-1]:
            newContent += ".\n\t\t"
        else:
            newContent += ", "

    newContent += templateContent[positions[1] + len(tags.doiTags[1]): positions[2]]
    newContent += "https://doi.org/10.1177/2056305115610141"
    newContent += templateContent[positions[2] + len(tags.doiTags[2]): positions[3]]
    newContent += date
    newContent += templateContent[positions[3] + len(tags.doiTags[3]):]

    file.write(newContent + "\n\n\n")
