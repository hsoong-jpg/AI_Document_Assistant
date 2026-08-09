css = '''
<style>

.chat-message {
    padding: 15px;
    border-radius: 14px;
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
}

.chat-message .avatar {
    width: 45px;
    height: 45px;
    min-width: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    margin-right: 12px;
    background-color: white;
}

.chat-message .message {
    flex: 1;
    padding: 5px 10px;
    line-height: 1.5;
}


/* USER */

.chat-message.user {
    background-color: #6FB3F2 !important;
}

.chat-message.user .message {
    color: #000000 !important;
}


/* BOT */

.chat-message.bot {
    background-color: #081978 !important;
}

.chat-message.bot .message {
    color: #FFFFFF !important;
}

</style>
'''


bot_template = '''
<div class="chat-message bot"
     style="background-color: #081978; color: white;">

    <div class="avatar">
        🤖
    </div>

    <div class="message"
         style="color: white;">

        {{MSG}}

    </div>
</div>
'''


user_template = '''
<div class="chat-message user"
     style="background-color: #6FB3F2; color: black;">

    <div class="avatar">
        🧑‍🔧
    </div>

    <div class="message"
         style="color: black;">

        {{MSG}}

    </div>
</div>
'''