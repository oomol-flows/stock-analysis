// "in", "out" is the default node key.
// Redefine the name and type of the node, change it manually below.
// Click on the gear(⚙) to configure the input output UI

export default async function(inputs, context) {

  // inputs.in -> help you get node input value
  console.log(inputs.in)

  // // This API can help preview several types of files
  // context.preview({
  //   // type -> "image","video", "audio", "markdown", "table", "iframe"
  //   type: "image",
  //   data: payload,
  // });
  return { out: null };
}
