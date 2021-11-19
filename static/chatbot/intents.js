function getBotResponse(input) {

    // Simple responses
    if (input == "hello" || input == "hi" || input == "hey") {
        return "Hello there! How can I help you?";
    } else if (input == "Hello, how's it going?") {
        return "Great! What can I do for you today?";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else if (input == "recent pisb event") {
        return "CTD";
    } else if (input == "recent pisb event dates"){
        return ["Following are the dates of CTD events", "1 - NCC - 23rd July 2021, 9-11 pm", "2 - RC - 25th July 2021, 9-11 pm", "3 - InQuizitive - 25th July 2021, 6-7 pm", "4 - NTH - 24th July 2021, 9 pm"];
    }
    else {
        return "Try asking something else!";
    }
}