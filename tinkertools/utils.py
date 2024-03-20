from enum import Flag

INTERP_STATS = [1, 2, 3, 8, 16, 17, 18, 19, 20, 21, 22, 27, 29, 36, 37, 54, 61, 71, 74, 90, 91, 92, 93, 94, 95, 96, 97, 100, 101, 102, 103, 104, 105, 
    106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 
    134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 
    162, 163, 164, 165, 166, 167, 168, 201, 204, 205, 206, 207, 208, 214, 216, 217, 218, 219, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234,
    238, 239, 240, 241, 242, 243, 244, 245, 276, 277, 278, 279, 280, 281, 282, 284, 285, 286, 287, 294, 311, 315, 316, 317, 318, 319, 343, 364, 
    374, 375, 379, 380, 381, 382, 383, 475, 476, 477, 478, 479, 480, 481, 482, 483]

STAT = {
    0 : 'None',
    1 : 'MaxHealth',
    2 : 'Mass',
    3 : 'AttackSpeed',
    4 : 'Breed',
    5 : 'Organization',
    6 : 'Team',
    7 : 'State',
    8 : 'Duration',
    9 : 'MapFlags',
    10 : 'ProfessionLevel',
    11 : 'PreviousHealth',
    12 : 'Mesh',
    13 : 'Anim',
    14 : 'Name',
    15 : 'Info',
    16 : 'Strength',
    17 : 'Agility',
    18 : 'Stamina',
    19 : 'Intelligence',
    20 : 'Sense',
    21 : 'Psychic',
    22 : 'AMS',
    23 : 'StaticInstance',
    24 : 'MaxMass',
    25 : 'StaticType',
    26 : 'Energy',
    27 : 'Health',
    28 : 'Height',
    29 : 'DMS',
    30 : 'Can',
    31 : 'Face',
    32 : 'HairMesh',
    33 : 'Faction',
    34 : 'DeadTimer',
    35 : 'AccessCount',
    36 : 'AttackCount',
    37 : 'TitleLevel',
    38 : 'BackMesh',
    39 : 'ShoulderMesh',
    40 : 'AlienXP',
    41 : 'FabricType',
    42 : 'CATMesh',
    43 : 'ParentType',
    44 : 'ParentInstance',
    45 : 'BeltSlots',
    46 : 'BandolierSlots',
    47 : 'Girth',
    48 : 'ClanLevel',
    49 : 'InsuranceTime',
    50 : 'InventoryTimeout',
    51 : 'AggDef',
    52 : 'XP',
    53 : 'IP',
    54 : 'Level',
    55 : 'InventoryId',
    56 : 'TimeSinceCreation',
    57 : 'LastXP',
    58 : 'Age',
    59 : 'Gender',
    60 : 'Profession',
    61 : 'Credits',
    62 : 'Alignment',
    63 : 'Attitude',
    64 : 'HeadMesh',
    65 : 'HairTexture',
    66 : 'ShoulderTexture',
    67 : 'HairColourRGB',
    68 : 'NumConstructedQuest',
    69 : 'MaxConstructedQuest',
    70 : 'SpeedPenalty',
    71 : 'TotalMass',
    72 : 'ItemType',
    73 : 'RepairDifficulty',
    74 : 'Value',
    75 : 'NanoStrain',
    76 : 'ItemClass',
    77 : 'RepairSkill',
    78 : 'CurrentMass',
    79 : 'Icon',
    80 : 'PrimaryItemType',
    81 : 'PrimaryItemInstance',
    82 : 'SecondaryItemType',
    83 : 'SecondaryItemInstance',
    84 : 'UserType',
    85 : 'UserInstance',
    86 : 'AreaType',
    87 : 'AreaInstance',
    88 : 'DefaultSlot',
    89 : 'Breed2',
    90 : 'ProjectileAC',
    91 : 'MeleeAC',
    92 : 'EnergyAC',
    93 : 'ChemicalAC',
    94 : 'RadiationAC',
    95 : 'ColdAC',
    96 : 'PoisonAC',
    97 : 'FireAC',
    98 : 'StateAction',
    99 : 'ItemAnim',
    100 : 'MartialArts',
    101 : 'MultiMelee',
    102 : '1hBlunt',
    103 : '1hEdged',
    104 : 'MeleeEnergy',
    105 : '2hEdged',
    106 : 'Piercing',
    107 : '2hBlunt',
    108 : 'SharpObjects',
    109 : 'Grenade',
    110 : 'HeavyWeapons',
    111 : 'Bow',
    112 : 'Pistol',
    113 : 'Rifle',
    114 : 'MG_SMG',
    115 : 'Shotgun',
    116 : 'AssaultRifle',
    117 : 'VehicleWater',
    118 : 'MeleeInit',
    119 : 'RangedInit',
    120 : 'PhysicalInit',
    121 : 'BowSpecialAttack',
    122 : 'SensoryImprovement',
    123 : 'FirstAid',
    124 : 'Treatment',
    125 : 'MechanicalEngineering',
    126 : 'ElectricalEngineering',
    127 : 'MaterialMetamorphose',
    128 : 'BiologicalMetamorphose',
    129 : 'PsychologicalModification',
    130 : 'MaterialCreation',
    131 : 'SpaceTime',
    132 : 'NanoPool',
    133 : 'RangedEnergy',
    134 : 'MultiRanged',
    135 : 'TrapDisarm',
    136 : 'Perception',
    137 : 'Adventuring',
    138 : 'Swimming',
    139 : 'VehicleAir',
    140 : 'MapNavigation',
    141 : 'Tutoring',
    142 : 'Brawl',
    143 : 'Riposte',
    144 : 'Dimach',
    145 : 'Parry',
    146 : 'SneakAttack',
    147 : 'FastAttack',
    148 : 'Burst',
    149 : 'NanoInit',
    150 : 'FlingShot',
    151 : 'AimedShot',
    152 : 'BodyDevelopment',
    153 : 'DuckExplosions',
    154 : 'DodgeRanged',
    155 : 'EvadeClose',
    156 : 'RunSpeed',
    157 : 'QuantumFT',
    158 : 'WeaponSmithing',
    159 : 'Pharmaceuticals',
    160 : 'NanoProgramming',
    161 : 'ComputerLiteracy',
    162 : 'Psychology',
    163 : 'Chemistry',
    164 : 'Concealment',
    165 : 'BreakingEntry',
    166 : 'VehicleGround',
    167 : 'FullAuto',
    168 : 'NanoResist',
    169 : 'AlienLevel',
    170 : 'HealthChangeBest',
    171 : 'HealthChangeWorst',
    172 : 'HealthChange',
    173 : 'CurrentMovementMode',
    174 : 'PrevMovementMode',
    175 : 'AutoLockTimeDefault',
    176 : 'AutoUnlockTimeDefault',
    177 : 'MoreFlags',
    178 : 'AlienNextXP',
    179 : 'NPCFlags',
    180 : 'CurrentNCU',
    181 : 'MaxNCU',
    182 : 'Specialization',
    183 : 'EffectIcon',
    184 : 'BuildingType',
    185 : 'BuildingInstance',
    186 : 'CardOwnerType',
    187 : 'CardOwnerInstance',
    188 : 'BuildingComplexInst',
    189 : 'ExitInstance',
    190 : 'NextDoorInBuilding',
    191 : 'LastConcretePlayfieldInstance',
    192 : 'ExtenalPlayfieldInstance',
    193 : 'ExtenalDoorInstance',
    194 : 'InPlay',
    195 : 'AccessKey',
    196 : 'ConflictReputation',
    197 : 'OrientationMode',
    198 : 'SessionTime',
    199 : 'ResetPoints',
    200 : 'Conformity',
    201 : 'Aggressiveness',
    202 : 'Stability',
    203 : 'Extroverty',
    204 : 'Taunt',
    205 : 'ReflectProjectileAC',
    206 : 'ReflectMeleeAC',
    207 : 'ReflectEnergyAC',
    208 : 'ReflectChemicalAC',
    209 : 'WeaponMesh',
    210 : 'RechargeDelay',
    211 : 'EquipDelay',
    212 : 'MaxEnergy',
    213 : 'TeamFaction',
    214 : 'CurrentNano',
    215 : 'GmLevel',
    216 : 'ReflectRadiationAC',
    217 : 'ReflectColdAC',
    218 : 'ReflectNanoAC',
    219 : 'ReflectFireAC',
    220 : 'CurrBodyLocation',
    221 : 'MaxNanoEnergy',
    222 : 'AccumulatedDamage',
    223 : 'CanChangeClothes',
    224 : 'Features',
    225 : 'ReflectPoisonAC',
    226 : 'ShieldProjectileAC',
    227 : 'ShieldMeleeAC',
    228 : 'ShieldEnergyAC',
    229 : 'ShieldChemicalAC',
    230 : 'ShieldRadiationAC',
    231 : 'ShieldColdAC',
    232 : 'ShieldNanoAC',
    233 : 'ShieldFireAC',
    234 : 'ShieldPoisonAC',
    235 : 'BerserkMode',
    236 : 'InsurancePercentage',
    237 : 'ChangeSideCount',
    238 : 'AbsorbProjectileAC',
    239 : 'AbsorbMeleeAC',
    240 : 'AbsorbEnergyAC',
    241 : 'AbsorbChemicalAC',
    242 : 'AbsorbRadiationAC',
    243 : 'AbsorbColdAC',
    244 : 'AbsorbFireAC',
    245 : 'AbsorbPoisonAC',
    246 : 'AbsorbNanoAC',
    247 : 'TemporarySkillReduction',
    248 : 'BirthDate',
    249 : 'LastSaved',
    250 : 'SoundVolume',
    251 : 'CheckPetType',
    252 : 'MetersWalked',
    253 : 'QuestLevelsSolved',
    254 : 'MonsterLevelsKilled',
    255 : 'PvPLevelsKilled',
    256 : 'MissionBits1',
    257 : 'MissionBits2',
    258 : 'AccessGrant',
    259 : 'DoorFlags',
    260 : 'ClanHierarchy',
    261 : 'QuestStat',
    262 : 'ClientActivated',
    263 : 'PersonalResearchLevel',
    264 : 'GlobalResearchLevel',
    265 : 'PersonalResearchGoal',
    266 : 'GlobalResearchGoal',
    267 : 'TurnSpeed',
    268 : 'LiquidType',
    269 : 'GatherSound',
    270 : 'CastSound',
    271 : 'TravelSound',
    272 : 'HitSound',
    273 : 'SecondaryItemTemplate',
    274 : 'EquippedWeapons',
    275 : 'XPKillRange',
    276 : 'AddAllOffense',
    277 : 'AddAllDefense',
    278 : 'ProjectileDamageModifier',
    279 : 'MeleeDamageModifier',
    280 : 'EnergyDamageModifier',
    281 : 'ChemicalDamageModifier',
    282 : 'RadiationDamageModifier',
    283 : 'ItemHateValue',
    284 : 'CriticalBonus',
    285 : 'MaxDamage',
    286 : 'MinDamage',
    287 : 'AttackRange',
    288 : 'HateValueModifier',
    289 : 'TrapDifficulty',
    290 : 'StatOne',
    291 : 'NumAttackEffects',
    292 : 'DefaultAttackType',
    293 : 'ItemSkill',
    294 : 'AttackDelay',
    295 : 'ItemOpposedSkill',
    296 : 'ItemSIS',
    297 : 'InteractionRadius',
    298 : 'Slot',
    299 : 'LockDifficulty',
    300 : 'Members',
    301 : 'MinMembers',
    302 : 'ClanPrice',
    303 : 'ClanUpkeep',
    304 : 'ClanType',
    305 : 'ClanInstance',
    306 : 'VoteCount',
    307 : 'MemberType',
    308 : 'MemberInstance',
    309 : 'GlobalClanType',
    310 : 'GlobalClanInstance',
    311 : 'ColdDamageModifier',
    312 : 'ClanUpkeepInterval',
    313 : 'TimeSinceUpkeep',
    314 : 'ClanFinalized',
    315 : 'NanoDamageModifier',
    316 : 'FireDamageModifier',
    317 : 'PoisonDamageModifier',
    318 : 'NanoCost',
    319 : 'XPModifier',
    320 : 'BreedLimit',
    321 : 'GenderLimit',
    322 : 'LevelLimit',
    323 : 'PlayerKilling',
    324 : 'TeamAllowed',
    325 : 'WeaponDisallowedType',
    326 : 'WeaponDisallowedInstance',
    327 : 'Taboo',
    328 : 'Compulsion',
    329 : 'SkillDisabled',
    330 : 'ClanItemType',
    331 : 'ClanItemInstance',
    332 : 'DebuffFormula',
    333 : 'PvPRating',
    334 : 'SavedXP',
    335 : 'DoorBlockTime',
    336 : 'OverrideTexture',
    337 : 'OverrideMaterial',
    338 : 'DeathReason',
    339 : 'DamageType',
    340 : 'BrainType',
    341 : 'XPBonus',
    342 : 'HealInterval',
    343 : 'HealDelta',
    344 : 'MonsterTexture',
    345 : 'HasAlwaysLootable',
    346 : 'TradeLimit',
    347 : 'FaceTexture',
    348 : 'SpecialCondition',
    349 : 'AutoAttackFlags',
    350 : 'NextXP',
    351 : 'TeleportPauseMilliSeconds',
    352 : 'SISCap',
    353 : 'AnimSet',
    354 : 'AttackType',
    355 : 'WornItem',
    356 : 'NPCHash',
    357 : 'CollisionRadius',
    358 : 'OuterRadius',
    359 : 'ShapeShift',
    360 : 'Scale',
    361 : 'HitEffectType',
    362 : 'ResurrectDestination',
    363 : 'NanoInterval',
    364 : 'NanoDelta',
    365 : 'ReclaimItem',
    366 : 'GatherEffectType',
    367 : 'VisualBreed',
    368 : 'VisualProfession',
    369 : 'VisualGender',
    370 : 'RitualTargetInst',
    371 : 'SkillTimeOnSelectedTarget',
    372 : 'LastSaveXP',
    373 : 'ExtendedTime',
    374 : 'BurstRecharge',
    375 : 'FullAutoRecharge',
    376 : 'GatherAbstractAnim',
    377 : 'CastTargetAbstractAnim',
    378 : 'CastSelfAbstractAnim',
    379 : 'CriticalIncrease',
    380 : 'WeaponRange',
    381 : 'NanoRange',
    382 : 'SkillLockModifier',
    383 : 'NanoInterruptModifier',
    384 : 'EntranceStyles',
    385 : 'ChanceOfBreakOnSpellAttack',
    386 : 'ChanceOfBreakOnDebuff',
    387 : 'DieAnim',
    388 : 'TowerType',
    389 : 'Expansion',
    390 : 'LowresMesh',
    391 : 'CriticalResistance',
    392 : 'OldTimeExist',
    393 : 'ResistModifier',
    394 : 'ChestFlags',
    395 : 'PrimaryTemplateID',
    396 : 'NumberOfItems',
    397 : 'SelectedTargetType',
    398 : 'CorpseHash',
    399 : 'AmmoName',
    400 : 'Rotation',
    401 : 'CATAnim',
    402 : 'CATAnimFlags',
    403 : 'DisplayCATAnim',
    404 : 'DisplayCATMesh',
    405 : 'NanoSchool',
    406 : 'NanoSpeed',
    407 : 'NanoPoints',
    408 : 'TrainSkill',
    409 : 'TrainSkillCost',
    410 : 'InFight',
    411 : 'NextFormula',
    412 : 'MultipleCount',
    413 : 'EffectType',
    414 : 'ImpactEffectType',
    415 : 'CorpseType',
    416 : 'CorpseInstance',
    417 : 'CorpseAnimKey',
    418 : 'UnarmedTemplateInstance',
    419 : 'TracerEffectType',
    420 : 'AmmoType',
    421 : 'CharRadius',
    422 : 'ChanceOfBreakOnAttack',
    423 : 'CurrentState',
    424 : 'ArmorType',
    425 : 'RestModifier',
    426 : 'BuyModifier',
    427 : 'SellModifier',
    428 : 'CastEffectType',
    429 : 'NPCBrainState',
    430 : 'WaitState',
    431 : 'SelectedTarget',
    432 : 'ErrorCode',
    433 : 'OwnerInstance',
    434 : 'CharState',
    435 : 'ReadOnly',
    436 : 'DamageType2',
    437 : 'CollideCheckInterval',
    438 : 'PlayfieldType',
    439 : 'NPCCommand',
    440 : 'InitiativeType',
    441 : 'CharTmp1',
    442 : 'CharTmp2',
    443 : 'CharTmp3',
    444 : 'CharTmp4',
    445 : 'NPCCommandArg',
    446 : 'NameTemplate',
    447 : 'DesiredTargetDistance',
    448 : 'VicinityRange',
    449 : 'NPCIsSurrendering',
    450 : 'StateMachine',
    451 : 'NPCSurrenderInstance',
    452 : 'NPCHasPatrolList',
    453 : 'NPCVicinityChars',
    454 : 'ProximityRangeOutdoors',
    455 : 'NPCFamily',
    456 : 'CommandRange',
    457 : 'NPCHatelistSize',
    458 : 'NPCNumPets',
    459 : 'ODMinSizeAdd',
    460 : 'EffectRed',
    461 : 'EffectGreen',
    462 : 'EffectBlue',
    463 : 'ODMaxSizeAdd',
    464 : 'DurationModifier',
    465 : 'NPCCryForHelpRange',
    466 : 'LOSHeight',
    467 : 'SLZoneProtection',
    468 : 'PetReq2',
    469 : 'PetReq3',
    470 : 'MapUpgrades',
    471 : 'MapFlags1',
    472 : 'MapFlags2',
    473 : 'FixtureFlags',
    474 : 'FallDamage',
    475 : 'MaxReflectedProjectileAC',
    476 : 'MaxReflectedMeleeAC',
    477 : 'MaxReflectedEnergyAC',
    478 : 'MaxReflectedChemicalAC',
    479 : 'MaxReflectedRadiationAC',
    480 : 'MaxReflectedColdAC',
    481 : 'MaxReflectedNanoAC',
    482 : 'MaxReflectedFireAC',
    483 : 'MaxReflectedPoisonAC',
    484 : 'ProximityRangeIndoors',
    485 : 'PetReqVal1',
    486 : 'PetReqVal2',
    487 : 'PetReqVal3',
    488 : 'TargetFacing',
    489 : 'Backstab',
    490 : 'OriginatorType',
    491 : 'QuestInstance',
    492 : 'QuestIndex1',
    493 : 'QuestIndex2',
    494 : 'QuestIndex3',
    495 : 'QuestIndex4',
    496 : 'QuestIndex5',
    497 : 'QTDungeonInstance',
    498 : 'QTNumMonsters',
    499 : 'QTKilledMonsters',
    500 : 'AnimPos',
    501 : 'AnimPlay',
    502 : 'AnimSpeed',
    503 : 'QTKillNumMonsterID1',
    504 : 'QTKillNumMonsterCount1',
    505 : 'QTKillNumMonsterID2',
    506 : 'QTKillNumMonsterCount2',
    507 : 'QTKillNumMonsterID3',
    508 : 'QTKillNumMonsterCount3',
    509 : 'QuestIndex0',
    510 : 'QuestTimeout',
    511 : 'TowerNPCHash',
    512 : 'PetType',
    513 : 'OnTowerCreation',
    514 : 'OwnedTowers',
    515 : 'TowerInstance',
    516 : 'AttackShield',
    517 : 'SpecialAttackShield',
    518 : 'NPCVicinityPlayers',
    519 : 'NPCUseFightModeRegenRate',
    520 : 'RandomNumberRoll',
    521 : 'SocialStatus',
    522 : 'LastRnd',
    523 : 'AttackDelayCap',
    524 : 'RechargeDelayCap',
    525 : 'RemainingHealth',
    526 : 'RemainingNano',
    527 : 'TargetDistance',
    528 : 'TeamLevel',
    529 : 'NumberOnHateList',
    530 : 'ConditionState',
    531 : 'ExpansionPlayfield',
    532 : 'ShadowBreed',
    533 : 'NPCFovStatus',
    534 : 'DudChance',
    535 : 'HealModifier',
    536 : 'NanoDamage',
    537 : 'NanoVulnerability',
    538 : 'MaxBeneficialSkill',
    539 : 'ProcInitiative1',
    540 : 'ProcInitiative2',
    541 : 'ProcInitiative3',
    542 : 'ProcInitiative4',
    543 : 'FactionModifier',
    545 : 'Flag265',
    546 : 'StackingLine2',
    547 : 'StackingLine3',
    548 : 'StackingLine4',
    549 : 'StackingLine5',
    550 : 'StackingLine6',
    551 : 'StackingOrder',
    552 : 'ProcNano1',
    553 : 'ProcNano2',
    554 : 'ProcNano3',
    555 : 'ProcNano4',
    556 : 'ProcChance1',
    557 : 'ProcChance2',
    558 : 'ProcChance3',
    559 : 'ProcChance4',
    560 : 'OTArmedForces',
    561 : 'ClanSentinels',
    562 : 'OTMed',
    563 : 'ClanGaia',
    564 : 'OTTrans',
    565 : 'ClanVanguards',
    566 : 'GaurdianOfShadows',
    567 : 'OTFollowers',
    568 : 'OTOperator',
    569 : 'OTUnredeemed',
    570 : 'ClanDevoted',
    571 : 'ClanConserver',
    572 : 'ClanRedeemed',
    573 : 'SK',
    574 : 'LastSK',
    575 : 'NextSK',
    576 : 'PlayerOptions',
    577 : 'LastPerkResetTime',
    578 : 'CurrentTime',
    579 : 'ShadowBreedTemplate',
    580 : 'NPCVicinityFamily',
    581 : 'NPCScriptAMSScale',
    582 : 'ApartmentsAllowed',
    583 : 'ApartmentsOwned',
    584 : 'ApartmentAccessCard',
    585 : 'MapFlags3',
    586 : 'MapFlags4',
    587 : 'NumberOfTeamMembers',
    588 : 'ActionCategory',
    589 : 'CurrentPlayfield',
    590 : 'DistrictNano',
    591 : 'DistrictNanoInterval',
    592 : 'UnsavedXP',
    593 : 'RegainXP',
    594 : 'TempSaveTeamID',
    595 : 'TempSavePlayfield',
    596 : 'TempSaveX',
    597 : 'TempSaveY',
    598 : 'ExtendedFlags',
    599 : 'ShopPrice',
    600 : 'NewbieHP',
    601 : 'HPLevelUp',
    602 : 'HPPerSkill',
    603 : 'NewbieNP',
    604 : 'NPLevelUp',
    605 : 'NPPerSkill',
    606 : 'MaxShopItems',
    607 : 'PlayerID',
    608 : 'ShopRent',
    609 : 'SynergyHash',
    610 : 'ShopFlags',
    611 : 'ShopLastUsed',
    612 : 'ShopType',
    613 : 'LockDownTime',
    614 : 'LeaderLockDownTime',
    615 : 'InvadersKilled',
    616 : 'KilledByInvaders',
    618 : 'Flag323',
    620 : 'HouseTemplate',
    621 : 'FireDamage',
    622 : 'ColdDamage',
    623 : 'MeleeDamage',
    624 : 'ProjectileDamage',
    625 : 'PoisonDamage',
    626 : 'RadiationDamage',
    627 : 'EnergyDamage',
    628 : 'ChemicalDamage',
    629 : 'TotalDamage',
    630 : 'TrackProjectileDamage',
    631 : 'TrackMeleeDamage',
    632 : 'TrackEnergyDamage',
    633 : 'TrackChemicalDamage',
    634 : 'TrackRadiationDamage',
    635 : 'TrackColdDamage',
    636 : 'TrackPoisonDamage',
    637 : 'TrackFireDamage',
    638 : 'NPCSpellArg1',
    639 : 'NPCSpellRet1',
    640 : 'CityInstance',
    641 : 'DistanceToSpawnpoint',
    642 : 'CityTerminalRechargePercent',
    643 : 'CooldownTime1',
    644 : 'CooldownTime2',
    645 : 'CooldownTime3',
    646 : 'CooldownTime4',
    647 : 'CooldownTime5',
    648 : 'CooldownTime6',
    651 : 'AdvantageHash1',
    652 : 'AdvantageHash2',
    653 : 'AdvantageHash3',
    654 : 'AdvantageHash4',
    655 : 'AdvantageHash5',
    656 : 'ShopIndex',
    657 : 'ShopID',
    658 : 'IsVehicle',
    659 : 'DamageToNano',
    660 : 'AccountFlags',
    661 : 'DamageToNano2',
    662 : 'MechData',
    663 : 'PointValue',
    664 : 'VehicleAC',
    665 : 'VehicleDamage',
    666 : 'VehicleHealth',
    667 : 'VehicleSpeed',
    668 : 'BattlestationFaction',
    669 : 'VictoryPoints',
    670 : 'BattlestationRep',
    671 : 'PetState',
    672 : 'PaidPoints',
    674 : 'PvpDuelKills',
    675 : 'PvpDuelDeaths',
    676 : 'PvpProfessionDuelKills',
    677 : 'PvpProfessionDuelDeaths',
    682 : 'PvpSoloScore',
    683 : 'PvpTeamScore',
    684 : 'PvpDuelScore',
    685 : 'MissionBits14',
    686 : 'MissionBits15',
    687 : 'ConfirmUseTextInstance',
    688 : 'ItemRarity',
    689 : 'HealReactivityMultiplier',
    690 : 'RHandWeaponType',
    691 : 'FullIPR',
    695 : 'IccCommendations',
    696 : 'FreelancersIncTokens',
    700 : 'ItemSeed',
    701 : 'ItemLevel',
    702 : 'ItemTemplateID',
    703 : 'ItemTemplateID2',
    704 : 'ItemCategoryID',
    768 : 'HasKnubotData',
    800 : 'QuestBoothDifficulty',
    801 : 'QuestASMinimumRange',
    802 : 'QuestASMaximumRange',
    888 : 'VisualLODLevel',
    889 : 'TargetDistanceChange',
    900 : 'TideRequiredDynelID',
    999 : 'StreamCheckMagic',
    1001 : 'Type',
    1002 : 'Instance',
    649 : 'Unknown649',
    10207 : 'Unknown10207',
}

REQUIREMENTS = {
    -1 : 'Any',
    102 : '1hBlunt',
    103 : '1hEdged',
    107 : '2hBlunt',
    105 : '2hEdged',
    22 : 'AMS',
    660 : 'AccountFlags',
    137 : 'Adventuring',
    51 : 'AggDef',
    17 : 'Agility',
    151 : 'AimedShot',
    169 : 'AlienLevel',
    62 : 'Alignment',
    582 : 'ApartmentsAllowed',
    583 : 'ApartmentsOwned',
    116 : 'AssaultRifle',
    354 : 'AttackType',
    349 : 'AutoAttackFlags',
    668 : 'BattlestationFaction',
    128 : 'BiologicalMetamorphose',
    152 : 'BodyDevelopment',
    111 : 'Bow',
    121 : 'BowSpecialAttack',
    142 : 'Brawl',
    165 : 'BreakingEntry',
    4 : 'Breed',
    148 : 'Burst',
    434 : 'CharState',
    441 : 'CharTmp1',
    251 : 'CheckPetType',
    93 : 'ChemicalAC',
    628 : 'ChemicalDamage',
    163 : 'Chemistry',
    571 : 'ClanConserver',
    570 : 'ClanDevoted',
    48 : 'ClanLevel',
    572 : 'ClanRedeemed',
    95 : 'ColdAC',
    622 : 'ColdDamage',
    161 : 'ComputerLiteracy',
    164 : 'Concealment',
    61 : 'Credits',
    173 : 'CurrentMovementMode',
    214 : 'CurrentNano',
    589 : 'CurrentPlayfield',
    144 : 'Dimach',
    154 : 'DodgeRanged',
    153 : 'DuckExplosions',
    126 : 'ElectricalEngineering',
    92 : 'EnergyAC',
    627 : 'EnergyDamage',
    280 : 'EnergyDamageModifier',
    274 : 'EquippedWeapons',
    155 : 'EvadeClose',
    389 : 'Expansion',
    531 : 'ExpansionPlayfield',
    33 : 'Faction',
    147 : 'FastAttack',
    224 : 'Features',
    97 : 'FireAC',
    621 : 'FireDamage',
    123 : 'FirstAid',
    618 : 'Flag323',
    150 : 'FlingShot',
    167 : 'FullAuto',
    566 : 'GaurdianOfShadows',
    59 : 'Gender',
    47 : 'Girth',
    215 : 'GmLevel',
    109 : 'Grenade',
    67 : 'HairColourRGB',
    65 : 'HairTexture',
    64 : 'HeadMesh',
    27 : 'Health',
    110 : 'HeavyWeapons',
    410 : 'InFight',
    19 : 'Intelligence',
    702 : 'ItemTemplateID',
    522 : 'LastRnd',
    54 : 'Level',
    114 : 'MG_SMG',
    471 : 'MapFlags1',
    472 : 'MapFlags2',
    586 : 'MapFlags4',
    140 : 'MapNavigation',
    470 : 'MapUpgrades',
    100 : 'MartialArts',
    130 : 'MaterialCreation',
    127 : 'MaterialMetamorphose',
    1 : 'MaxHealth',
    221 : 'MaxNanoEnergy',
    662 : 'MechData',
    125 : 'MechanicalEngineering',
    91 : 'MeleeAC',
    623 : 'MeleeDamage',
    104 : 'MeleeEnergy',
    118 : 'MeleeInit',
    300 : 'Members',
    12 : 'Mesh',
    301 : 'MinMembers',
    685 : 'MissionBits14',
    686 : 'MissionBits15',
    257 : 'MissionBits2',
    101 : 'MultiMelee',
    134 : 'MultiRanged',
    455 : 'NPCFamily',
    457 : 'NPCHatelistSize',
    132 : 'NanoPool',
    160 : 'NanoProgramming',
    168 : 'NanoResist',
    75 : 'NanoStrain',
    0 : 'None',
    587 : 'NumberOfTeamMembers',
    567 : 'OTFollowers',
    568 : 'OTOperator',
    569 : 'OTUnredeemed',
    5 : 'Organization',
    145 : 'Parry',
    136 : 'Perception',
    159 : 'Pharmaceuticals',
    106 : 'Piercing',
    112 : 'Pistol',
    438 : 'PlayfieldType',
    96 : 'PoisonAC',
    625 : 'PoisonDamage',
    60 : 'Profession',
    10 : 'ProfessionLevel',
    90 : 'ProjectileAC',
    624 : 'ProjectileDamage',
    21 : 'Psychic',
    129 : 'PsychologicalModification',
    162 : 'Psychology',
    157 : 'QuantumFT',
    690 : 'RHandWeaponType',
    94 : 'RadiationAC',
    626 : 'RadiationDamage',
    520 : 'RandomNumberRoll',
    133 : 'RangedEnergy',
    119 : 'RangedInit',
    208 : 'ReflectChemicalAC',
    217 : 'ReflectColdAC',
    207 : 'ReflectEnergyAC',
    219 : 'ReflectFireAC',
    206 : 'ReflectMeleeAC',
    205 : 'ReflectProjectileAC',
    216 : 'ReflectRadiationAC',
    525 : 'RemainingHealth',
    526 : 'RemainingNano',
    113 : 'Rifle',
    143 : 'Riposte',
    156 : 'RunSpeed',
    467 : 'SLZoneProtection',
    360 : 'Scale',
    83 : 'SecondaryItemInstance',
    273 : 'SecondaryItemTemplate',
    82 : 'SecondaryItemType',
    431 : 'SelectedTarget',
    397 : 'SelectedTargetType',
    20 : 'Sense',
    122 : 'SensoryImprovement',
    198 : 'SessionTime',
    579 : 'ShadowBreedTemplate',
    359 : 'ShapeShift',
    108 : 'SharpObjects',
    229 : 'ShieldChemicalAC',
    231 : 'ShieldColdAC',
    228 : 'ShieldEnergyAC',
    233 : 'ShieldFireAC',
    227 : 'ShieldMeleeAC',
    234 : 'ShieldPoisonAC',
    226 : 'ShieldProjectileAC',
    230 : 'ShieldRadiationAC',
    115 : 'Shotgun',
    146 : 'SneakAttack',
    521 : 'SocialStatus',
    131 : 'SpaceTime',
    182 : 'Specialization',
    18 : 'Stamina',
    16 : 'Strength',
    527 : 'TargetDistance',
    889 : 'TargetDistanceChange',
    488 : 'TargetFacing',
    204 : 'Taunt',
    6 : 'Team',
    213 : 'TeamFaction',
    247 : 'TemporarySkillReduction',
    37 : 'TitleLevel',
    124 : 'Treatment',
    141 : 'Tutoring',
    139 : 'VehicleAir',
    166 : 'VehicleGround',
    117 : 'VehicleWater',
    669 : 'VictoryPoints',
    368 : 'VisualProfession',
    430 : 'WaitState',
    158 : 'WeaponSmithing',
    355 : 'WornItem',
    52 : 'XP',
    319 : 'XPModifier'
}

SPELL_MODIFIED_STATS = {
    -1 : 'Any',
    102 : '1hBlunt',
    103 : '1hEdged',
    107 : '2hBlunt',
    105 : '2hEdged',
    22 : 'AMS',
    241 : 'AbsorbChemicalAC',
    243 : 'AbsorbColdAC',
    240 : 'AbsorbEnergyAC',
    244 : 'AbsorbFireAC',
    239 : 'AbsorbMeleeAC',
    245 : 'AbsorbPoisonAC',
    238 : 'AbsorbProjectileAC',
    242 : 'AbsorbRadiationAC',
    35 : 'AccessCount',
    277 : 'AddAllDefense',
    276 : 'AddAllOffense',
    137 : 'Adventuring',
    51 : 'AggDef',
    201 : 'Aggressiveness',
    17 : 'Agility',
    151 : 'AimedShot',
    169 : 'AlienLevel',
    40 : 'AlienXP',
    62 : 'Alignment',
    583 : 'ApartmentsOwned',
    116 : 'AssaultRifle',
    516 : 'AttackShield',
    45 : 'BeltSlots',
    128 : 'BiologicalMetamorphose',
    152 : 'BodyDevelopment',
    111 : 'Bow',
    121 : 'BowSpecialAttack',
    142 : 'Brawl',
    165 : 'BreakingEntry',
    148 : 'Burst',
    251 : 'CheckPetType',
    93 : 'ChemicalAC',
    281 : 'ChemicalDamageModifier',
    163 : 'Chemistry',
    571 : 'ClanConserver',
    570 : 'ClanDevoted',
    302 : 'ClanPrice',
    572 : 'ClanRedeemed',
    95 : 'ColdAC',
    311 : 'ColdDamageModifier',
    161 : 'ComputerLiteracy',
    164 : 'Concealment',
    61 : 'Credits',
    379 : 'CriticalIncrease',
    391 : 'CriticalResistance',
    180 : 'CurrentNCU',
    214 : 'CurrentNano',
    659 : 'DamageToNano',
    661 : 'DamageToNano2',
    339 : 'DamageType',
    144 : 'Dimach',
    154 : 'DodgeRanged',
    153 : 'DuckExplosions',
    126 : 'ElectricalEngineering',
    26 : 'Energy',
    92 : 'EnergyAC',
    280 : 'EnergyDamageModifier',
    155 : 'EvadeClose',
    147 : 'FastAttack',
    224 : 'Features',
    97 : 'FireAC',
    316 : 'FireDamageModifier',
    123 : 'FirstAid',
    545 : 'Flag265',
    618 : 'Flag323',
    150 : 'FlingShot',
    696 : 'FreelancersIncTokens',
    167 : 'FullAuto',
    691 : 'FullIPR',
    566 : 'GaurdianOfShadows',
    47 : 'Girth',
    215 : 'GmLevel',
    109 : 'Grenade',
    65 : 'HairTexture',
    343 : 'HealDelta',
    342 : 'HealInterval',
    535 : 'HealModifier',
    689 : 'HealReactivityMultiplier',
    27 : 'Health',
    110 : 'HeavyWeapons',
    53 : 'IP',
    695 : 'IccCommendations',
    410 : 'InFight',
    236 : 'InsurancePercentage',
    19 : 'Intelligence',
    54 : 'Level',
    114 : 'MG_SMG',
    471 : 'MapFlags1',
    472 : 'MapFlags2',
    585 : 'MapFlags3',
    586 : 'MapFlags4',
    140 : 'MapNavigation',
    470 : 'MapUpgrades',
    100 : 'MartialArts',
    130 : 'MaterialCreation',
    127 : 'MaterialMetamorphose',
    1 : 'MaxHealth',
    181 : 'MaxNCU',
    221 : 'MaxNanoEnergy',
    478 : 'MaxReflectedChemicalAC',
    480 : 'MaxReflectedColdAC',
    477 : 'MaxReflectedEnergyAC',
    482 : 'MaxReflectedFireAC',
    476 : 'MaxReflectedMeleeAC',
    481 : 'MaxReflectedNanoAC',
    483 : 'MaxReflectedPoisonAC',
    475 : 'MaxReflectedProjectileAC',
    479 : 'MaxReflectedRadiationAC',
    125 : 'MechanicalEngineering',
    91 : 'MeleeAC',
    279 : 'MeleeDamageModifier',
    104 : 'MeleeEnergy',
    118 : 'MeleeInit',
    301 : 'MinMembers',
    256 : 'MissionBits1',
    686 : 'MissionBits15',
    257 : 'MissionBits2',
    101 : 'MultiMelee',
    134 : 'MultiRanged',
    465 : 'NPCCryForHelpRange',
    179 : 'NPCFlags',
    318 : 'NanoCost',
    536 : 'NanoDamage',
    315 : 'NanoDamageModifier',
    364 : 'NanoDelta',
    149 : 'NanoInit',
    383 : 'NanoInterruptModifier',
    363 : 'NanoInterval',
    407 : 'NanoPoints',
    132 : 'NanoPool',
    160 : 'NanoProgramming',
    381 : 'NanoRange',
    168 : 'NanoResist',
    75 : 'NanoStrain',
    537 : 'NanoVulnerability',
    0 : 'None',
    567 : 'OTFollowers',
    568 : 'OTOperator',
    569 : 'OTUnredeemed',
    145 : 'Parry',
    136 : 'Perception',
    468 : 'PetReq2',
    469 : 'PetReq3',
    485 : 'PetReqVal1',
    486 : 'PetReqVal2',
    487 : 'PetReqVal3',
    512 : 'PetType',
    159 : 'Pharmaceuticals',
    120 : 'PhysicalInit',
    106 : 'Piercing',
    112 : 'Pistol',
    96 : 'PoisonAC',
    317 : 'PoisonDamageModifier',
    556 : 'ProcChance1',
    557 : 'ProcChance2',
    539 : 'ProcInitiative1',
    540 : 'ProcInitiative2',
    552 : 'ProcNano1',
    553 : 'ProcNano2',
    90 : 'ProjectileAC',
    278 : 'ProjectileDamageModifier',
    454 : 'ProximityRangeOutdoors',
    21 : 'Psychic',
    129 : 'PsychologicalModification',
    162 : 'Psychology',
    682 : 'PvpSoloScore',
    683 : 'PvpTeamScore',
    157 : 'QuantumFT',
    94 : 'RadiationAC',
    282 : 'RadiationDamageModifier',
    133 : 'RangedEnergy',
    119 : 'RangedInit',
    208 : 'ReflectChemicalAC',
    217 : 'ReflectColdAC',
    207 : 'ReflectEnergyAC',
    219 : 'ReflectFireAC',
    206 : 'ReflectMeleeAC',
    218 : 'ReflectNanoAC',
    225 : 'ReflectPoisonAC',
    205 : 'ReflectProjectileAC',
    216 : 'ReflectRadiationAC',
    593 : 'RegainXP',
    199 : 'ResetPoints',
    113 : 'Rifle',
    143 : 'Riposte',
    156 : 'RunSpeed',
    467 : 'SLZoneProtection',
    360 : 'Scale',
    20 : 'Sense',
    122 : 'SensoryImprovement',
    198 : 'SessionTime',
    532 : 'ShadowBreed',
    359 : 'ShapeShift',
    108 : 'SharpObjects',
    229 : 'ShieldChemicalAC',
    231 : 'ShieldColdAC',
    228 : 'ShieldEnergyAC',
    233 : 'ShieldFireAC',
    227 : 'ShieldMeleeAC',
    232 : 'ShieldNanoAC',
    234 : 'ShieldPoisonAC',
    226 : 'ShieldProjectileAC',
    230 : 'ShieldRadiationAC',
    115 : 'Shotgun',
    39 : 'ShoulderMesh',
    382 : 'SkillLockModifier',
    146 : 'SneakAttack',
    131 : 'SpaceTime',
    517 : 'SpecialAttackShield',
    18 : 'Stamina',
    16 : 'Strength',
    138 : 'Swimming',
    135 : 'TrapDisarm',
    124 : 'Treatment',
    141 : 'Tutoring',
    139 : 'VehicleAir',
    166 : 'VehicleGround',
    117 : 'VehicleWater',
    669 : 'VictoryPoints',
    368 : 'VisualProfession',
    380 : 'WeaponRange',
    158 : 'WeaponSmithing',
    355 : 'WornItem',
    52 : 'XP',
    319 : 'XPModifier'
}

PROFESSION = {
    0 : 'Unknown',
    1 : 'Soldier',
    2 : 'MartialArtist',
    3 : 'Engineer',
    4 : 'Fixer',
    5 : 'Agent',
    6 : 'Adventurer',
    7 : 'Trader',
    8 : 'Bureaucrat',
    9 : 'Enforcer',
    10 : 'Doctor',
    11 : 'NanoTechnician',
    12 : 'MetaPhysicist',
    13 : 'Monster',
    14 : 'Keeper',
    15 : 'Shade'
}

AMMOTYPE = {
    0 : 'None',
    1 : 'Energy',
    2 : 'Bullets',
    3 : 'FlameThrower',
    4 : 'ShotgunShells',
    5 : 'Arrows',
    6 : 'LauncherGrenades',
    7 : 'Rockets',
    8 : 'Missiles',
    10: 'Infinite'
}

TEXTURELOCATION = {
    0 : 'Hands',
    1 : 'Body',
    2 : 'Feet',
    3 : 'Arms',
    4 : 'Legs'
}

NANOSCHOOL = {
    1 : 'Combat',
    2 : 'Medical',
    3 : 'Protection',
    4 : 'Psi',
    5 : 'Space',
}

NPCFAMILY = {
    0 : 'Human',
    95 : 'RoboticPet',
    96 : 'HealingConstruct',
    97 : 'AttackConstruct',
    98 : 'MesmerizingConstruct',
    157 : 'ControlTower',
}

FACTION = {
    0 : 'Neutral',
    1 : 'Clan',
    2 : 'Omni'
}

GENDER = {
    0 : 'Unknown',
    1 : 'Uni',
    2 : 'Male',
    3 : 'Female',
}

BREED = {
    0 : 'Unknown',
    1 : 'Solitus',
    2 : 'Opifex',
    3 : 'Nanomage',
    4 : 'Atrox',
    7 : 'HumanMonster',
}

class SPECIALIZATION_FLAG(Flag):
    NONE = 0
    First = 2**0
    Second = 2**1
    Third = 2**2
    Fourth = 2**3
    Bit5 = 2**5
    Bit6 = 2**6
    Bit7 = 2**7
    Bit8 = 2**8

class ACTION_FLAG(Flag):
    NONE = 0
    Bit0 = 2**0
    Fighting = 2**1
    Moving = 2**2
    Falling = 2**3
    ImplantAccess = 2**4
    Chat = 2**5
    SkillTime = 2**6
    Concealment = 2**7
    CryForHelp = 2**8
    VicinityInfo = 2**9
    Attack = 2**10
    OnGrid = 2**11
    BankAccess = 2**12
    Zoning = 2**13
    Help = 2**14
    WalkOnLand = 2**15
    Bit15 = 2**16
    SwimInWater = 2**17
    FlyInAir = 2**18
    Terminate = 2**19
    Bit20 = 2**20
    Bit21 = 2**21
    Bit22 = 2**22
    Bit23 = 2**23
    Anon = 2**24
    Bit25 = 2**25
    PvP = 2**26
    Bit27 = 2**27
    Bit28 = 2**28
    Bit29 = 2**29
    Bit30 = 2**30
    Bit31 = 2**31

class NANO_NONE_FLAG(Flag):
    NONE = 0
    Visible = 2**0
    NoResistCannotFumble = 2**1
    IsShapeChange = 2**2
    BreakOnAttack = 2**3
    TurnOnUse = 2**4
    BreakOnDebuff = 2**5
    BreakOnInterval = 2**6
    BreakOnSpellAttack = 2**7
    NoRemoveNoNCUFriendly = 2**8
    TellCollision = 2**9
    NoSelectionIndicator = 2**10
    UseEmptyDestruct = 2**11
    NoIIR = 2**12
    NoResist = 2**13
    NotRemovable = 2**14
    IsHostile = 2**15
    IsBuff = 2**16
    IsDebuff = 2**17
    PlayshiftRequirements = 2**18
    NoTimerNotify = 2**19
    NoTimeoutNotify = 2**20
    DontRemoveOnDeath = 2**21
    DontBreakOnAttack = 2**22
    CannotRefresh = 2**23
    IsHidden = 2**24
    ClassDebuffMMBM = 2**25
    ClassDebuffMCTS = 2**26
    ClassDebuffPMSI = 2**27
    ClassCombatDebuff = 2**28
    ClassAoE = 2**29
    ClassRootOrSnare = 2**30
    WantCollision = 2**31

class ITEM_NONE_FLAG(Flag):
    NONE = 0
    Visible = 2**0
    ModifiedDescription = 2**1
    ModifiedName = 2**2
    CanBeTemplateItem = 2**3
    TurnOnUse = 2**4
    HasMultipleCount = 2**5
    Locked = 2**6
    Open = 2**7
    ItemSocialArmour = 2**8
    TellCollision = 2**9
    NoSelectionIndicator = 2**10
    UseEmptyDestruct = 2**11
    Stationary = 2**12
    Repulsive = 2**13
    DefaultTarget = 2**14
    ItemTextureOverride = 2**15
    Null = 2**16
    HasAnimation = 2**17
    HasRotation = 2**18
    WantCollision = 2**19
    WantSignals = 2**20
    HasSentFirstIIR = 2**21
    HasEnergy = 2**22
    MirrorInLeftHand = 2**23
    IllegalClan = 2**24
    IllegalOmni = 2**25
    NoDrop = 2**26
    Unique = 2**27
    CanBeAttacked = 2**28
    DisableFalling = 2**29
    HasDamage = 2**30
    DisableStatelCollision = 2**31


class CANFLAG(Flag):
    NONE = 0
    Carry = 2**0
    Sit = 2**1
    Wear = 2**2
    Use = 2**3
    ConfirmUse = 2**4
    Consume = 2**5
    TutorChip = 2**6
    TutorDevice = 2**7
    BreakingAndEntering = 2**8
    Stackable = 2**9
    NoAmmo = 2**10
    Burst = 2**11
    FlingShot = 2**12
    FullAuto = 2**13
    AimedShot = 2**14
    Bow = 2**15
    ThrowAttack = 2**16
    SneakAttack = 2**17
    FastAttack = 2**18
    DisarmTraps = 2**19
    AutoSelect = 2**20
    ApplyOnFriendly = 2**21
    ApplyOnHostile = 2**22
    ApplyOnSelf = 2**23
    CantSplit = 2**24
    Brawl = 2**25
    Dimach = 2**26
    EnableHandAttractors = 2**27
    CanBeWornWithSocialArmor = 2**28
    CanParryRiposite = 2**29
    CanBeParriedRiposited = 2**30
    ApplyOnFightingTarget = 2**31


class EXPANSION_FLAG(Flag):
    NONE = 0
    NotumWars = 2**0
    Shadowlands = 2**1
    ShadowlandsPreorder = 2**2
    AlienInvasion = 2**3
    AlienInvasionPreorder = 2**4
    LostEden = 2**5
    LostEdenPreorder = 2**6
    LexacyOfXan = 2**7
    LegacyOfXanPreorder = 2**8

class WORN_ITEM(Flag):
    BasicCyberDeck = 2**0
    AugmentedCyberDeck = 2**1
    JobeCyberDeck = 2**2
    IzgimmerCyberDeck = 2**3
    GridArmor = 2**4
    SocialArmor = 2**5
    NanoDeck = 2**6
    MpSummonedWeapon = 2**7
    Bit8 = 2**8
    Bit9 = 2**9
    Bit10 = 2**10
    Bit11 = 2**11
    Bit12 = 2**12
    Bit13 = 2**13
    Bit14 = 2**14
    Bit15 = 2**15
    Bit16 = 2**16
    Bit17 = 2**17
    Bit18 = 2**18
    Bit19 = 2**19
    Bit20 = 2**20
    Bit21 = 2**21
    Bit22 = 2**22
    Bit23 = 2**23
    Bit24 = 2**24
    Bit25 = 2**25
    Bit26 = 2**26
    Bit27 = 2**27
    Bit28 = 2**28
    Bit29 = 2**29
    Bit30 = 2**30
    Bit31 = 2**31

EXPANSION_PLAYFIELD = {
    0 : 'Rubika',
    1 : 'Shadowlands'
}

class SL_ZONE_PROTECTION(Flag):
    Adonis = 2**0
    Penumbra = 2**1
    Inferno = 2**2
    Pandemonium = 2**3

TARGET = {
    1 : 'Self',
    2 : 'User',
    3 : 'Target',
    4 : 'Item',
    5 : 'Transfer',
    6 : 'Ground',
    7 : 'PersonSpotted',
    8 : 'Attacker',
    9 : 'Victim',
    10 : 'Master',
    11 : 'EnemyHealer',
    12 : 'FriendAttacker',
    13 : 'CommandTarget',
    14 : 'FightTarget',
    15 : 'ScaryEnemy',
    16 : 'FollowTarget',
    17 : 'LastOpponent',
    18 : 'PersonLeaving',
    19 : 'PersonLost',
    20 : 'Pet',
    21 : 'Area',
    22 : 'Commander',
    23 : 'SelectedTarget',
    24 : 'LastFollowTarget',
}

class WEAPON_SLOT(Flag):
    NONE = 0
    Bit0 = 2**0
    Hud1 = 2**1
    Hud3 = 2**2
    Util1 = 2**3
    Util2 = 2**4
    Util3 = 2**5
    RightHand = 2**6
    Deck = 2**7
    LeftHand = 2**8
    Deck1 = 2**9
    Deck2 = 2**10
    Deck3 = 2**11
    Deck4 = 2**12
    Deck5 = 2**13
    Deck6 = 2**14
    Hud2 = 2**15

WEAPON_SLOT_POSITIONS = {
    0 : 'None',
    1 : 'Hud1',
    2 : 'Hud3',
    3 : 'Utils1',
    4 : 'Utils2',
    5 : 'Utils3',
    6 : 'RightHand',
    7 : 'Deck',
    8 : 'LeftHand',
    9 : 'Deck1',
    10 : 'Deck2',
    11 : 'Deck3',
    12 : 'Deck4',
    13 : 'Deck5',
    14 : 'Deck6',
    15 : 'Hud2',
}

class ARMOR_SLOT(Flag):
    NONE = 0
    Bit0 = 2**0
    Neck = 2**1
    Head = 2**2
    Back = 2**3
    RightShoulder = 2**4
    Chest = 2**5
    LeftShoulder = 2**6
    RightArm = 2**7
    Hands = 2**8
    LeftArm = 2**9
    RightWrist = 2**10
    Legs = 2**11
    LeftWrist = 2**12
    RightFinger = 2**13
    Feet = 2**14
    LeftFinger = 2**15
    PerkAction = 2**31

ARMOR_SLOT_POSITION = {
    0 : 'None',
    1 : 'Neck',
    2 : 'Head',
    3 : 'Back',
    4 : 'RightShoulder',
    5 : 'Chest',
    6 : 'LeftShoulder',
    7 : 'RightArm',
    8 : 'Hands',
    9 : 'LeftArm',
    10 : 'RightWrist',
    11 : 'Legs',
    12 : 'LeftWrist',
    13 : 'RightFinger',
    14 : 'Feet',
    15 : 'LeftFinger'
}

class IMPLANT_SLOT(Flag):
    NONE = 0
    Bit0 = 2**0
    Eyes = 2**1
    Head = 2**2
    Ears = 2**3
    RightArm = 2**4
    Chest = 2**5
    LeftArm = 2**6
    RightWrist = 2**7
    Waist = 2**8
    LeftWrist = 2**9
    RightHand = 2**10
    Legs = 2**11
    LeftHand = 2**12
    Feet = 2**13

IMPLANT_SLOT_POSITION = {
    0 : 'None',
    1 : 'Eyes',
    2 : 'Head',
    3 : 'Ears',
    4 : 'RightArm',
    5 : 'Chest',
    6 : 'LeftArm',
    7 : 'RightWrist',
    8 : 'Waist',
    9 : 'LeftWrist',
    10 : 'RightHand',
    11 : 'Legs',
    12 : 'LeftHand',
    13 : 'Feet'
}

TOWER_TYPE = {
    0 : 'None',
    1 : 'Control',
    2 : 'Offensive',
    3 : 'Stun',
    4 : 'Support',
    5 : 'AntiAir',
    6 : 'Pulse',
}

ITEM_CLASS = {
    0 : 'None',
    1 : 'Weapon',
    2 : 'Armor',
    3 : 'Implant',
    4 : 'Monster',
    5 : 'Spirit',
}

GROUPING_OPERATOR = {
    3 : 'Or',
    4 : 'And',
    42 : 'Not',      
}

FUNCTION_OPERATOR = {
    15 : 'Unknown15',
    31 : 'ItemWorn',
    32 : 'ItemNotWorn',
    33 : 'ItemWielded',
    34 : 'ItemNotWielded',
    35 : 'OwnsNano',
    36 : 'NotOwnsNano',
    50 : 'IsSameAs',
    88 : 'UseLocation',
    91 : 'RunningNano',
    92 : 'RunningNanoLine',
    93 : 'PerkTrained',
    94 : 'PerkLocked',
    97 : 'PerkNotLocked',
    98 : 'True',
    99 : 'False',
    101 : 'NotRunningNano',
    102 : 'NotRunningNanoLine',
    103 : 'PerkNotTrained',
    104 : 'SpawnedFromHash',
    106 : 'NeedFreeInventorySlots',
    108 : 'OwnsItem',
    109 : 'NotOwnsItem',
    117 : 'HasQuestHash',
    127 : 'CheckNcu',
    85 : 'StatSameAsSelectedTarget',
    130 : 'StatEqualStat',
    131 : 'StatLessThanStat',
    132 : 'StatGreaterThanStat',
    133 : 'StatNotEqualStat',
}

USE_ON_OPERATOR = {
    18 : 'Target',
    19 : 'Self',
    21 : 'SecondaryItem',
    26 : 'User',
    100 : 'Caster',
    110 : 'FightingTarget',
}

STATE_OPERATOR = {
    44 : 'IsNpc',
    45 : 'IsFighting',
    134 : 'IsNotFighting',
    66 : 'HaveNoRegularPets',
    70 : 'IsFlying',
    80 : 'IsTowerCreateAllowed',
    83 : 'CanDisableDefenseShield',
    86 : 'IsPlayerOrPlayerControlledPet',
    89 : 'IsFalling',
    111 : 'NotInVehicle',
    112 : 'FlyingAllowed',
    114 : 'IsLandmineArmed',
    115 : 'CanPlaceLandmine',
    116 : 'IsInOrganization',
    118 : 'IsOwnPet',
    119 : 'InGracePeriod',
    120 : 'InLcaLevelRange',
    121 : 'IsInRaid',
    122 : 'IsBossNpc',
    123 : 'IsInDuel',
    124 : 'CanTeleport',
    125 : 'HasNotAnythingWorn',
    129 : 'UnknownOperator129',
    135 : 'AlliesInCombat',
    136 : 'AlliesNotInCombat',
    138 : 'InTeamWith',
}

STAT_OPERATOR = {
    0 : 'Equal',
    1 : 'LessThan',
    2 : 'GreaterThan',
    22 : 'BitSet',
    24 : 'NotEqual',
    107 : 'BitNotSet',
}

OPERATOR = {
    0 : 'StatEqual',
    1 : 'StatLessThan',
    2 : 'StatGreaterThan',
    22 : 'StatBitSet',
    24 : 'StatNotEqual',
    107 : 'StatBitNotSet',
    3 : 'Or',
    4 : 'And',
    42 : 'Not',
    44 : 'StateIsNpc',
    45 : 'StateIsFighting',
    134 : 'StateIsNotFighting',
    66 : 'StateHaveNoRegularPets',
    70 : 'StateIsFlying',
    80 : 'StateIsTowerCreateAllowed',
    83 : 'StateCanDisableDefenseShield',
    86 : 'StateIsPlayerOrPlayerControlledPet',
    89 : 'StateIsFalling',
    111 : 'StateNotInVehicle',
    112 : 'StateFlyingAllowed',
    114 : 'StateIsLandmineArmed',
    115 : 'StateCanPlaceLandmine',
    116 : 'StateIsInOrganization',
    118 : 'StateIsOwnPet',
    119 : 'StateInGracePeriod',
    120 : 'StateInLcaLevelRange',
    121 : 'StateIsInRaid',
    122 : 'StateIsBossNpc',
    123 : 'StateIsInDuel',
    124 : 'StateCanTeleport',
    125 : 'StateHasNotAnythingWorn',
    135 : 'Unknown135',
    136 : 'StateAlliesNotInCombat',
    138 : 'StateInTeamWith',
    15 : 'Unknown15', 
    31 : 'ItemWorn',
    32 : 'ItemNotWorn',
    33 : 'ItemWielded',
    34 : 'ItemNotWielded',
    35 : 'OwnsNano',
    36 : 'NotOwnsNano',
    50 : 'IsSameAs',
    88 : 'UseLocation',
    91 : 'RunningNano',
    92 : 'RunningNanoLine',
    93 : 'PerkTrained',
    94 : 'PerkLocked',
    97 : 'PerkNotLocked',
    98 : 'True',
    99 : 'False',
    101 : 'NotRunningNano',
    102 : 'NotRunningNanoLine',
    103 : 'PerkNotTrained',
    104 : 'SpawnedFromHash',
    106 : 'NeedFreeInventorySlots',
    108 : 'OwnsItem',
    109 : 'NotOwnsItem',
    117 : 'HasQuestHash',
    127 : 'CheckNcu',
    128 : 'Unknown128',
    85 : 'StatSameAsSelectedTarget',
    130 : 'StatEqualStat',
    131 : 'StatLessThanStat',
    132 : 'StatGreaterThanStat',
    133 : 'StatNotEqualStat',
    18 : 'OnTarget',
    19 : 'OnSelf',
    21 : 'OnSecondaryItem',
    26 : 'OnUser',
    100 : 'OnCaster',
    110 : 'OnFightingTarget',
    129 : 'UnknownOperator129',
}

ITEMCLASS = {
    0 : "None",
    1 : "Weapon",
    2 : "Armor",
    3 : "Implant",
}

TEMPLATE_EVENT = {
    0 : "Use",
    1 : "Repair",
    2 : "Wield",
    3 : "TargetInVicinity",
    4 : "UseItemOnTarget",
    5 : "Hit",
    6 : "NPCWear",
    7 : "Create",
    8 : "Effects",
    9 : "Run",
    10 : "Activate",
    12 : "StartEffect",
    13 : "EndEffect",
    14 : "Wear",
    15 : "UseFailed",
    16 : "Enter",
    18 : "Open",
    19 : "Close",
    20 : "Terminate",
    21 : "Unknown",
    23 : "EndCollide",
    24 : "FriendlyInVicinity",
    25 : "EnemyInVicinity",
    26 : "PersonalModifier",
    27 : "Failure",
    28 : "Cancellation",
    37 : "Trade"
}

TEMPLATE_ACTION = {
    0 : "Any",
    1 : "Get",
    3 : "Use",
    5 : "UseItemOnItem",
    6 : "Wear",
    7 : "Remove",
    8 : "Wield",
    15 : "Idle",
    32 : "UseItemOnItem2",
    111 : "TriggerTargetInVicinity",
    136 : "PlayshiftRequirements",
}

SPELL_FORMATS = {
    53002 : 'Hit {Stat} for {MinValue} to {MaxValue} | {TickCount}x @ {TickInterval}s',
    53003 : 'Animation effect, A={A} B={B} C={C} D={D} E={E}',
    53012 : 'Modify {Stat} | {Amount}',
    53014 : 'Modify {Stat} for {Duration}s | {Amount}',
    53016 : 'Teleport to {X}x{Z}x{Y} in playfield {Playfield}',
    53019 : 'Upload {NanoID}',
    53025 : 'Animation, A={A} B={B} C={C}',
    53026 : 'Set {Skill} | {Amount}',
    53028 : 'Add Skill {Skill} | {Amount}',
    53030 : 'Gfx effect',
    53032 : 'Save character',
    53033 : 'Lock skill {Skill} for {Duration}s',
    53035 : 'Head mesh, A={A} B={B}',
    53037 : 'Back Mesh, A={A} B={B}',
    53038 : 'Apply shoulder mesh A={A} B={B}',
    53039 : 'Apply texture {Texture} to {Location}',
    53044 : 'System text: {Text}',
    53045 : 'Modify {Stat} | {Amount}',
    53051 : 'Cast {NanoID}',
    53054 : 'Change body mesh, A={A}',
    53055 : 'Attractor Mesh, A={A} B={B}',
    53057 : 'Float text: {Text}',
    53060 : 'Temporarily change shape to {Shape}',
    53063 : 'Spawn QL{Quality} {MonsterHash} for {Duration}s',
    53064 : 'Spawn QL{Quality} {Item}',
    53065 : 'Attractor Effect A, A={A} B={B} C={C} D={D}',
    53066 : 'Cast {NanoID} on team',
    53067 : 'Change action {Action} restriction for {Duration}s',
    53068 : 'Restrict action {Action}',
    53069 : 'Change to next head',
    53070 : 'Change to previous head',
    53073 : 'Hit all {Stat} within {Radius}m for {MinAmount} to {MaxAmount}, modified by {ModifierStat}',
    53075 : 'Attractor Effect B, A={A} B={B} C={C} D={D}',
    53076 : 'Attractor Effect C, A={A} B={B} C={C} D={D}',
    53078 : 'Social animation: {Animation}',
    53079 : 'Change effect, A={A} B={B} C={C}',
    53082 : 'Teleport to {Playfield}, subgroup {SG}',
    53083 : 'Teleport to {Playfield}',
    53086 : 'Refresh model',
    53087 : 'Cast {NanoID} with radius {Radius}m',
    53089 : '{Chance}% chance to cast {NanoID}',
    53092 : 'Open bank',
    53100 : 'Equip monster weapon {Item}',
    53104 : 'NPC say {Message}',
    53105 : 'Remove {NanoStrain} nanos <= {NCU} NCU {Times} times',
    53107 : 'Run script {Script}',
    53109 : 'Enter apartment',
    53110 : 'Temporarily change {Stat} to {Value}',
    53115 : 'Display GUI element',
    53117 : 'Taunt {Amount} for {Duration}s',
    53118 : 'Pacify',
    53121 : 'Fear',
    53122 : 'Stun',
    53124 : '{Chance}% chance to spawn QL{Quality} item {Item}',
    53126 : 'Wipe hate list',
    53127 : 'Charm',
    53128 : 'Daze',
    53130 : 'Destroy item',
    53132 : 'Generate name',
    53133 : 'Set government type {Government}',
    53134 : 'Text: {Text}',
    53137 : 'Create apartment in {Playfield}',
    53138 : 'Enable flight',
    53139 : 'Set flag {Stat} {BitNum}',
    53140 : 'Clear flag {Stat} {BitNum}',
    53142 : 'Unknown',
    53144 : 'Teleport to last insurance point',
    53153 : 'Mezz',
    53154 : 'Teleport selected player to current location',
    53155 : 'Teleport team to current location',
    53162 : 'Resist {NanoStrain} | {Resistance}%',
    53164 : 'Save character',
    53166 : 'Generate name',
    53167 : 'Summon level {Level} pet for {Lifetime}s',
    53173 : 'Deploy to land control area',
    53175 : 'Modify {Stat} | {Amount}',
    53177 : 'Reduce strain {NanoStrain} by {Duration}s',
    53178 : 'Disable defensive shield',
    53181 : 'Summon pets',
    53182 : 'Add action: {UseItem}',
    53184 : 'Modify base {Stat} | {Percent}%',
    53185 : 'Hit {Stat} for {MinValue} to {MaxValue} and recover {DrainAmount}%',
    53187 : 'Lock perk {PerkID} for {Duration}s',
    53189 : 'Update {Skill}',
    53191 : '{Action}',
    53192 : 'Spawn QL{Quality} {Monster} corpse',
    53193 : 'Apply model {Model}',
    53196 : 'Hit {Stat} for {MinValue} to {MaxValue}, checks {ModifierStat}',
    53204 : 'Attractor Gfx Effect',
    53206 : 'If possible, cast {NanoID}',
    53208 : 'Set anchor',
    53209 : 'Teleport to anchor',
    53210 : 'Say {Message}',
    53213 : 'Control hate',
    53220 : 'Spawn QL {Quality} NPC {Spawnee}',
    53221 : 'Run script {Script} with parameters {A} {B} {C}',
    53222 : 'Join battlestation queue',
    53223 : 'Register control point',
    53224 : 'Add defensive proc {Proc} with {Chance}% chance to trigger',
    53225 : 'Destroy all humans',
    53226 : 'Spawn mission {Quest}',
    53227 : 'Add offensive proc {Proc} with {Chance}% chance to trigger',
    53228 : 'Cast {NanoID} on playfield',
    53229 : 'Complete mission {Quest}',
    53230 : 'Knock back within radius {Radius} with force {Power}',
    53231 : 'Enable raid lock for current playfield',
    53232 : 'Mind control',
    53233 : 'Instanced player city',
    53234 : 'Reset all perks',
    53235 : 'Create city guest key for {Playfield}',
    53236 : 'Remove strain {NanoStrain}',
    53237 : 'Modify buffed {Stat} | {Percent}%',
    53238 : 'Switch breed to {Breed} {Gender}',
    53239 : 'Change gender to {Gender}',
    53240 : 'Cast {NanoID} on all pets',
    53241 : 'Unknown',
    53242 : 'Cast {NanoID}',
    53243 : 'Unknown',
    53244 : 'Global message: {Message}',
    53247 : '{Text}',
    53248 : 'Remove cooldown, Entity={Entity} Value={Value}',
    53249 : 'Transfer {Credits} credits from {TakeFrom}',
    53250 : 'Delete quest {QuestId}',
    53251 : 'Fail mission {Quest}',
    53252 : 'Send mail',
    53253 : 'End fight',
    53254 : 'Try sneak on {Target}', 
}

class WEAPON_TYPE(Flag):
    NONE = 0
    Fists = 2**0
    Melee = 2**1
    Ranged = 2**2
    Bow = 2**3
    SMG = 2**4
    OneHandEdge = 2**5
    OneHandBlunt = 2**6
    TwoHandEdge = 2**7
    TwoHandBlunt = 2**8
    Piercing = 2**9
    Pistol = 2**10
    AssaultRifle = 2**11
    Rifle = 2**12
    Shotgun = 2**13
    Energy = 2**14
    Grenade = 2**15
    HeavyWeapons = 2**16
    Bit17 = 2**17
    Bit18 = 2**18
    Bit19 = 2**19
    Bit20 = 2**20
    Bit21 = 2**21
    Bit22 = 2**22
    TestItem = 2**23
    Bit24 = 2**24
    Bit25 = 2**25
    Bit26 = 2**26
    Bit27 = 2**27
    Bit28 = 2**28
    Bit29 = 2**29
    Bit30 = 2**30
    Bit31 = 2**31

class SL_ZONE_PROTECTION(Flag):
    Adonis = 0
    Penumbra = 2**0
    Inferno = 2**1
    Pandemonium = 2**2






