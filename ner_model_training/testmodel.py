import spacy

def main():
    # Load trained model
    model = spacy.load("./model")

    # Text to extract entities from
    text = """Responsible for developing bespoke applications for the business utilising industry standard modern technologies (React, .NET Core, Node)

Produce well-structured and efficient code

Consider efficient database design, being mindful of how we can leverage business data across different applications

Assist in choosing the appropriate technology for each business requirement.

Consider security aspects of the solution design

Work collaboratively with Business Analysts and use git repositories and pull requests to manage workflow

Work with Azure DevOps to manage CI/CDWhy Greencore?We are a leading manufacturer of convenience food in the UK and our purpose is to make every day taste better.

Join us and be part of our great team.

We supply all of the major supermarkets in the UK. We also supply convenience and travel retail outlets, discounters, coffee shops, foodservice and other retailers. We have strong market positions in a range of categories including sandwiches, salads, sushi chilled snacking, chilled ready meals, chilled soups and sauces, chilled quiche, ambient sauces and pickles, and frozen Yorkshire Puddings.

In FY22 we manufactured 795m sandwiches and other food to go products, 127m chilled prepared meals, and 249m bottles of cooking sauces, pickles and condiments. We carry out more than 10,600 direct to store deliveries each day. We have 21 world-class manufacturing units across 16 locations in the UK, with industry-leading technology and supply chain capabilities. We generated revenues of £1.7bn in FY22 and employ approximately 14,000 people.

We work hard to ensure that Greencore is a great place to work and our people truly are at the core. We’re committed to ensuring all our colleagues have development plans and strive to provide inspiring leadership – in fact, in the past year we’ve seen an 11% increase in the number of colleagues who would recommend Greencore as a place to work. Why not come join us?

We’re always looking for passionate and talented people who can help us drive our future success. To see how you can grow your career with Greencore, visit our careers website

https://(url removed)/ and find your future in food.

For further information go to (url removed) or follow Greencore on social media.To facilitate the development of software systems, links between software systems, configuration of software systems or the retrieval of data from software systems

What we’re looking for

Experience and strong fundamental understanding of front-end development (React, JavaScript, Typescript, jQuery, Bootstrap, Tailwind)

Experience and strong understanding of REST API development (C#, .NET Core, Entity Framework, Dependency Injection, Swagger)

Strong understanding of relational database design (SQL Server)

Experience with source control systems such as Git (BitBucket) and continuous integration/continuous deployment (Azure DevOps)

Desirables: Azure, Kubernetes, containerisation (Docker), SSIS, Azure Data Factory, IIS

What you’ll get in return

Competitive salary and job-related benefits

Holidays

Pension up to 8% matched

Company share save scheme

Greencore Qualifications

Exclusive Greencore employee discount platform

Access to a full Wellbeing Centre platformThroughout your time at Greencore, you will be supported with on the job training and development opportunities to further your career"""

    # Process the text
    doc = model(text.lower())

    # Print the entities
    for ent in doc.ents:
        print(f"{ent.text} ({ent.label_})")


    

if __name__ == "__main__":
    main()
