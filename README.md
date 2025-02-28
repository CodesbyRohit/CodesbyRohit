# CodesbyRohit

/**
 * @author CodesbyRohit
 * @version 1.0
 * @description GitHub profile README.md
 */

## About Me

```javascript
const username = "CodesbyRohit";
const interests = ["Web Development", "Java", "Python"];
let learning = "Python";
const collaboration = {
  type: ["Beginner-friendly projects", "Web applications"],
};
const contact = {
  instagram: "[www.instagram.com/peter3_rohit](https://www.google.com/search?q=https://www.instagram.com/peter3_rohit)",
};
const pronouns = "he/him";

console.log(`👋 Hi, I’m @${username}`);
console.log(`👀 I’m interested in ${interests.join(", ")}`);
console.log(`🌱 I’m currently learning ${learning}`);
console.log(`💞️ I’m looking to collaborate on ${collaboration.type.join(", ")}`);
console.log(`📫 How to reach me: ${contact.instagram}`);
console.log(`😄 Pronouns: ${pronouns}`);

FUN FACT
/**
 * @description A fun fact about the origin of the term "bug" in software.
 */
function displayFunFact() {
  const funFact = `The term "bug" to describe a software error came from a real bug! In 1947, Grace Hopper, a pioneer in computer science, discovered a moth stuck in the inner workings of a computer that was causing a malfunction. She jokingly referred to the issue as a "bug" and the term stuck!`;
  console.log(`⚡ Fun fact: ${funFact}`);
}

displayFunFact();
