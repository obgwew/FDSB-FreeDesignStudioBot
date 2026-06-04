#PREFIX:-roll
$cooldown[5s; ⏳ بطيء شوي! انتظر {time}]
$setVar[sides; $message[1]]

$if[$var[sides] == ]
  $setVar[sides; 6]
$endif

$if[$var[sides] < 2]
 $sendMessage[🟠 النرد يحتاج وجهين على الأقل!]
$else
  $sendMessage[🎲 $mention رمى نرداً من **$getVar[sides]** وجه — نتيجة: **$randomint[1; $getVar[sides]]**!]
$endif