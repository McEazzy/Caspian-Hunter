import spacy

text = """About the role

Unifacta Pty Ltd is seeking a talented Software Engineer to join our dynamic and innovative team based in Melbourne, Victoria. As a Software Engineer, you will play a crucial role in developing and enhancing our cutting-edge software solutions. This full-time position offers the opportunity to work alongside experienced professionals and contribute to the growth and success of our company.

We are a small team that work closely together and lean on each others skills and abilities regularly.

What you'll be doing

Collaborate with a small but dedicated team to design, develop, and implement software applications and features

Write clean, efficient, and well-documented code using the latest technologies and best practices

Participate in the entire software development lifecycle, including requirements gathering, design, testing, and deployment

Communicate with clients to understand requirements and translate into technical briefs.

Troubleshoot and debug existing applications to identify and resolve issues

Continually learn and stay up-to-date with the latest industry trends and technologies

Contribute to the development of innovative solutions to complex business problems

Assist various departments where necessary within the areas of your technical expertise, including On-Boarding and Support.

What we're looking for

3-5 years of experience in software development, either through internships, projects, or previous roles

Strong proficiency in front-end frameworks and technologies including JavaScript, CSS and HTML. React & React Native experience an advantage.

Experience collaborating with customers to solve problems

Excellent communication skills with the ability to bridge the gap between technical teams and business stakeholders.

Strong problem-solving and critical thinking skills

Excellent communication and collaboration abilities

Passion for staying up-to-date with the latest technologies and trends in the industry

Bachelor's degree in Computer Science, Software Engineering, or a related field, preferred but not necessary depending on experience

What we offer

At Unifacta, we believe in fostering a supportive and inclusive work environment that empowers our employees to thrive. We offer a range of benefits, including:

- Competitive salary and bonus structure
- Flexible work arrangements to support work-life balance
- Collaborative and innovative work culture"""

nlp = spacy.load("seek_ner")
doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)