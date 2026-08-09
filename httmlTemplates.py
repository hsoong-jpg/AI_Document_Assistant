
css = '''
<style>

.chat-message {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    margin-bottom: 12px;
    border-radius: 14px;
}

.chat-message.user {
    background-color: #2b313e;
}

.chat-message.bot {
    background-color: #475063;
}

.chat-message .avatar {
    width: 42px;
    height: 42px;
    min-width: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    background-color: #ffffff;
}

.chat-message .message {
    flex: 1;
    padding: 8px 4px;
    color: white;
    font-size: 15px;
    line-height: 1.6;
}

</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        🤖
    </div>
    <div class="message">
        {{MSG}}
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        🧑‍🔧
    </div>
    <div class="message">
        {{MSG}}
    </div>
</div>
'''

