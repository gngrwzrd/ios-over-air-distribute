<?php

/**
 * UUID generator class
 *
 * Generates valid RFC 4211 compliant Universally Unique IDentifiers (UUID) version 3, 4 and 5. 
 * UUIDs generated validate using the OSSP UUID Tool, and the output for named-based UUIDs are 
 * exactly the same. This is a pure PHP implementation.
 *
 * Usage:
 * 
 *   Name-based UUID:
 *
 *     $v3uuid = UUID::v3('1546058f-5a25-4334-85ae-e68f2a44bbaf', 'SomeRandomString');
 *     $v5uuid = UUID::v5(UUID::NS_URL, 'http://www.google.com/');
 *
 *   Pseudo-random UUID:
 *
 *     $v4uuid = UUID::v4();
 *
 *
 * Originally found at: http://www.php.net/manual/en/function.uniqid.php#94959
 *
 * @author Andrew Moore 
 *
 *
 * Modifications made by Henry Merriam <php@henrymerriam.com> on 2009-12-20:
 *
 *   + Added constants for predefined namespaces as defined in RFC 4211 Appendix C.
 *     + NS_DNS
 *     + NS_URL
 *     + NS_ISO_UID
 *     + NS_X500_DN
 *
 *   + Wrote this documentation comment.
 *
 */
class UUID {

    const NS_DNS     = '6ba7b810-9dad-11d1-80b4-00c04fd430c8'; // FQDN
    const NS_URL     = '6ba7b811-9dad-11d1-80b4-00c04fd430c8'; // URL
    const NS_ISO_OID = '6ba7b812-9dad-11d1-80b4-00c04fd430c8'; // ISO OID
    const NS_X500_DN = '6ba7b814-9dad-11d1-80b4-00c04fd430c8'; // X.500 DN (in DER or a text output format)

    public static function v3($namespace, $name) {

        if(!self::is_valid($namespace)) return false;

        // Get hexadecimal components of namespace
        $nhex = str_replace(array('-','{','}'), '', $namespace);

        // Binary Value
        $nstr = '';

        // Convert Namespace UUID to bits
        for($i = 0; $i < strlen($nhex); $i+=2) {
            $nstr .= chr(hexdec($nhex[$i].$nhex[$i+1]));
        }

        // Calculate hash value
        $hash = md5($nstr . $name);

        // Format and return UUID
        return sprintf('%08s-%04s-%04x-%04x-%12s',

            // 32 bits for "time_low"
            substr($hash, 0, 8),

            // 16 bits for "time_mid"
            substr($hash, 8, 4),

            // 16 bits for "time_hi_and_version",
            // four most significant bits holds version number 3
            (hexdec(substr($hash, 12, 4)) & 0x0fff) | 0x3000,

            // 16 bits, 8 bits for "clk_seq_hi_res",
            // 8 bits for "clk_seq_low",
            // two most significant bits holds zero and one for variant DCE1.1
            (hexdec(substr($hash, 16, 4)) & 0x3fff) | 0x8000,

            // 48 bits for "node"
            substr($hash, 20, 12)
        );

    }

    public static function v4() {

        return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',

            // 32 bits for "time_low"
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),

            // 16 bits for "time_mid"
            mt_rand(0, 0xffff),

            // 16 bits for "time_hi_and_version",
            // four most significant bits holds version number 4
            mt_rand(0, 0x0fff) | 0x4000,

            // 16 bits, 8 bits for "clk_seq_hi_res",
            // 8 bits for "clk_seq_low",
            // two most significant bits holds zero and one for variant DCE1.1
            mt_rand(0, 0x3fff) | 0x8000,

            // 48 bits for "node"
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        );

    }

    public static function v5($namespace, $name) {

        if(!self::is_valid($namespace)) return false;

        // Get hexadecimal components of namespace
        $nhex = str_replace(array('-','{','}'), '', $namespace);

        // Binary Value
        $nstr = '';

        // Convert Namespace UUID to bits
        for($i = 0; $i < strlen($nhex); $i+=2) {
            $nstr .= chr(hexdec($nhex[$i].$nhex[$i+1]));
        }

        // Calculate hash value
        $hash = sha1($nstr . $name);

        // Format and return UUID
        return sprintf('%08s-%04s-%04x-%04x-%12s',

            // 32 bits for "time_low"
            substr($hash, 0, 8),

            // 16 bits for "time_mid"
            substr($hash, 8, 4),

            // 16 bits for "time_hi_and_version",
            // four most significant bits holds version number 5
            (hexdec(substr($hash, 12, 4)) & 0x0fff) | 0x5000,

            // 16 bits, 8 bits for "clk_seq_hi_res",
            // 8 bits for "clk_seq_low",
            // two most significant bits holds zero and one for variant DCE1.1
            (hexdec(substr($hash, 16, 4)) & 0x3fff) | 0x8000,

            // 48 bits for "node"
            substr($hash, 20, 12)
        );

    }

    public static function is_valid($uuid) {
        return preg_match('/^\{?[0-9a-f]{8}\-?[0-9a-f]{4}\-?[0-9a-f]{4}\-?'.
            '[0-9a-f]{4}\-?[0-9a-f]{12}\}?$/i', $uuid) === 1;
    }

}