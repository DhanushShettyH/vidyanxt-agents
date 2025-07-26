const { onCall } = require("firebase-functions/v2/https");

exports.greet = onCall((data, context) => {
  const name = data.name;
  if (!name) {
    throw new functions.https.HttpsError('invalid-argument', 'Please provide a name.');
  }
  return { message: `Hello, ${name}!` };
});
